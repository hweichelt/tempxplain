"""Functionality for generating the explanations with asplain."""

from collections.abc import Iterable
from dataclasses import dataclass
from enum import Enum
from functools import cached_property
from pathlib import Path
from typing import Literal, cast, get_args

import clingo
from asplain import construct_program_graph, set_foil_ctl, set_model_subgraphs_ctl
from asplain.transformations.transformers import Transformation, apply_transformation_sequence
from asplain.utils.clingo import get_query_prg, symbols_to_prg
from clingo import SolveHandle, Symbol
from clingo.script import enable_python

from tempxplain.graph import TemporalExplanationGraph
from tempxplain.temporal import AtomType, atom_base, atom_time, atom_type, is_action, is_fluent
from tempxplain.utils.logging import get_logger
from tempxplain.utils.symbols import to_program

from .utils.io import read_file

log = get_logger("server.explain")

# Enable python for the clingo encodings in asplain using it
enable_python()

DEFAULT_COST_ENCODING = Path(__file__).parent / "encodings" / "cost" / "default.lp"
NUMBER_OF_EXPLANATIONS = 1
QUERY_NEGATION_PREFIX = "-"
MODEL_STRING_REF_TYPE = Literal["ref"]
MODEL_STRING_REF: Literal["ref"] = get_args(MODEL_STRING_REF_TYPE)[0]
MODEL_STRING_FOIL_TYPE = Literal["foil"]
MODEL_STRING_FOIL: Literal["foil"] = get_args(MODEL_STRING_FOIL_TYPE)[0]


class Model(Enum):
    """A model in the explanation graph."""

    REFERENCE = MODEL_STRING_REF
    FOIL = MODEL_STRING_FOIL


class ModelMembership(Enum):
    """The models an atom belongs to; the values of `Model` are a subset of the values here."""

    NONE = "none"
    REFERENCE = MODEL_STRING_REF
    FOIL = MODEL_STRING_FOIL
    BOTH = "both"

    @classmethod
    def from_model(cls, model: Model) -> "ModelMembership":
        """Construct a model membership from a model."""
        return cls(model.value)

    @classmethod
    def from_set(cls, models: set[Model]) -> "ModelMembership":
        """Construct a model membership from a set of models."""
        match list(models):
            case []:
                return cls.NONE
            case [model]:
                return cls.from_model(model)
            case _:
                return cls.BOTH

    def has(self, model: Model) -> bool:
        """Check whether the membership includes the given model."""
        return self in (ModelMembership.BOTH, ModelMembership.from_model(model))


@dataclass(frozen=True)
class Atom:
    """An atom in the explanation graph."""

    symbol: Symbol
    models: set[Model]

    @cached_property
    def type(self) -> AtomType:
        """The temporal type of the atom."""
        return atom_type(self.symbol)

    @cached_property
    def time(self) -> int | None:
        """The timestep of the atom, if it is timed."""
        return atom_time(self.symbol)

    @cached_property
    def base(self) -> Symbol:
        """
        The base atom of the atom, if it is timed.

        If it is static the atom itself is returned.
        """
        return atom_base(self.symbol)

    @cached_property
    def membership(self) -> ModelMembership:
        """The model membership of the atom."""
        return ModelMembership.from_set(self.models)

    @cached_property
    def is_fluent(self) -> bool:
        """Is the atom a fluent."""
        return is_fluent(self.symbol)

    @cached_property
    def is_action(self) -> bool:
        """Is the atom an action."""
        return is_action(self.symbol)

    def __hash__(self) -> int:
        """Hash based on symbol and its model membership."""
        return hash((self.symbol, self.membership))


@dataclass(frozen=True)
class Explanation:
    """Representation of an explanation graph."""

    symbols: set[Symbol]

    @cached_property
    def symbols_transformed(self) -> set[Symbol]:
        """The symbols of the explanation graph after temporal transformation."""
        return set(transform_temporal(self.symbols))

    @cached_property
    def program(self) -> str:
        """The explanation graph as a program string."""
        return to_program(self.symbols_transformed)

    @cached_property
    def graph(self) -> TemporalExplanationGraph:
        """The explanation graph."""
        return TemporalExplanationGraph.from_symbols(self.symbols_transformed)

    @cached_property
    def atoms(self) -> set[Atom]:
        """The atoms of the untransformed explanation graph with assigned model memberships."""
        return Explanation._explanation_symbols_to_atoms(self.symbols)

    @cached_property
    def atoms_transformed(self) -> set[Atom]:
        """The atoms of the transformed explanation graph with assigned model memberships."""
        return Explanation._explanation_symbols_to_atoms(self.symbols_transformed)

    @cached_property
    def atoms_static(self) -> set[Atom]:
        """The static atoms of the untransformed explanation graph."""
        return {a for a in self.atoms if a.time is None}

    @cached_property
    def atoms_transformed_timed(self) -> set[Atom]:
        """The timed atoms of the transformed explanation graph."""
        return {a for a in self.atoms_transformed if a.time is not None}

    @cached_property
    def fluents_transformed(self) -> set[Atom]:
        """The fluent atoms of the transformed explanation graph."""
        return {a for a in self.atoms_transformed_timed if a.is_fluent}

    @cached_property
    def actions_transformed(self) -> set[Atom]:
        """The action atoms of the transformed explanation graph."""
        return {a for a in self.atoms_transformed_timed if a.is_action}

    @cached_property
    def partitions_transformed(self) -> dict[int, set[Atom]]:
        """The partitions of the transformed explanation graph, indexed by timepoint."""
        partitions: dict[int, set[Atom]] = {}
        for atom in self.atoms_transformed_timed:
            if (timepoint := atom.time) is not None:
                partitions.setdefault(timepoint, set()).add(atom)
        return partitions

    @cached_property
    def interval_transformed(self) -> tuple[int, int]:
        """The time interval of the transformed explanation graph as a tuple (start, end)."""
        return min(self.partitions_transformed), max(self.partitions_transformed)

    @cached_property
    def length_transformed(self) -> int:
        """The length of the transformed explanation graph (the number of timepoints)."""
        return self.interval_transformed[1] - self.interval_transformed[0] + 1

    @cached_property
    def fluent_matrix_transformed(self) -> dict[Symbol, list[ModelMembership]]:
        """`Symbol` <-> `ModelMembership` matrix for fluents in the transformed explanation graph."""
        fluent_bases = {a.base for a in self.fluents_transformed}
        matrix = {a: [ModelMembership.NONE] * self.length_transformed for a in fluent_bases}
        for atom in self.fluents_transformed:
            assert atom.time is not None  # make sure time is not None
            matrix[atom.base][atom.time] = atom.membership
        return matrix

    @staticmethod
    def _explanation_symbols_to_atoms(symbols: set[Symbol]) -> set[Atom]:
        # collect symbols indicating model associations
        models: dict[Symbol, set[Model]] = {}
        for symbol in symbols:
            if symbol.match("model", 2):
                atom = symbol.arguments[0]
                model = Model(str(symbol.arguments[1]))
                models.setdefault(atom, set()).add(model)
        # collect node atoms, then associate them with their models
        atoms = set()
        for symbol in symbols:
            if symbol.match("node", 2) and str(symbol.arguments[1]) == "atom":
                atom = symbol.arguments[0]
                atom_models = models.get(atom, set())
                atoms.add(Atom(atom, atom_models))
        return atoms

    def get_model_state_at(self, model: Model, t: int) -> set[Symbol]:
        """Get the state of the domain world at given time `t` in the model `model`."""
        if t not in range(self.interval_transformed[0], self.interval_transformed[1] + 1):
            raise ValueError(f"Time {t} is out of range for the explanation interval {self.interval_transformed}")
        atoms_model_partition_t = {a.base for a in self.partitions_transformed[t] if a.membership.has(model)}
        atoms_static = {a.base for a in self.atoms_static}
        atoms_t = atoms_model_partition_t.union(atoms_static)
        log.info(f"Model state at t={t}: {[str(a) for a in atoms_t]}")
        return atoms_t


def parse_query_program(query: str) -> str:
    """Parse a query to get the query program for asplain."""
    query_include: list[Symbol] = []
    query_exclude: list[Symbol] = []
    for literal in query.strip().split():
        if literal.startswith(QUERY_NEGATION_PREFIX):
            query_exclude.append(clingo.parse_term(literal.removeprefix(QUERY_NEGATION_PREFIX)))
        else:
            query_include.append(clingo.parse_term(literal))
    return get_query_prg(query_include, query_exclude)


def parse_model(model_prg: str) -> list[str] | None:
    """
    Parse a model program to get the model's symbol strings.
    """
    if not model_prg.strip():
        return None
    control_model = clingo.Control(["1", "--warn=none"])
    control_model.add(model_prg)
    control_model.ground([("base", [])])
    with control_model.solve(yield_=True) as solve_handle:
        sh = cast(SolveHandle, solve_handle)
        symbols = set()
        for m in sh:
            symbols = {str(s) for s in m.symbols(atoms=True)}
        return list(symbols)


def transform_temporal(symbols: Iterable[Symbol]) -> list[Symbol]:
    """Transform the symbols of an explanation graph with the temporal pruning pipeline."""
    log.info("Applying temporal pruning")
    return apply_transformation_sequence(
        symbols,
        [
            Transformation.NO_MODEL,
            Transformation.FACT_RULES,
            Transformation.STATIC_DOMAIN_FACTS,
            Transformation.ORPHANS,
        ],
    )


def explanation(
    files: list[str],
    constants: dict[str, str],
    assumptions: set[tuple[str, bool]],
    model_program: str,
    query: str,
) -> Explanation:
    """Compute the explanation graph for a given program with query."""
    # Pre-Processing & Setup
    query_prg = parse_query_program(query)
    cost_prg = read_file(DEFAULT_COST_ENCODING)
    model_symbols = parse_model(model_program)
    control = clingo.Control(["--warn=none"])

    reference_pg = construct_program_graph(
        list(files),
        constants=constants,
        assumptions=list(assumptions),
        dynamic_tags_files=[],
    )
    model_subgraphs_ctl = set_model_subgraphs_ctl(pg=reference_pg, ctl=control, model_symbols=model_symbols)
    with model_subgraphs_ctl.solve(yield_=True) as solve_handle:
        sh = cast(SolveHandle, solve_handle)

        model_found = False
        for model in sh:
            model_found = True
            symbols = model.symbols(shown=True)
            reference_model_pg = symbols_to_prg(list(symbols))
            foil_ctl = set_foil_ctl(
                pg=reference_model_pg,
                query_prg=query_prg,
                cost_prg=cost_prg,
                number_of_foils=NUMBER_OF_EXPLANATIONS,
            )
            with foil_ctl.solve(yield_=True) as foil_handle:
                fh = cast(SolveHandle, foil_handle)

                for foil_model in fh:
                    if not foil_model.optimality_proven:
                        log.debug(f"Skipping non-optimal foil model {foil_model.number}")
                        continue
                    return Explanation(set(foil_model.symbols(shown=True)))
                log.warning("No foil found.")

        if not model_found:
            log.warning("UNSATISFIABLE. Will proceed to explain.")
            foil_ctl = set_foil_ctl(
                pg=reference_pg,
                query_prg=query_prg,
                cost_prg=cost_prg,
                number_of_foils=NUMBER_OF_EXPLANATIONS,
            )
            with foil_ctl.solve(yield_=True) as foil_handle:
                fh = cast(SolveHandle, foil_handle)

                for foil_model in fh:
                    if not foil_model.optimality_proven:
                        log.info(f"Skipping non-optimal foil model {foil_model.number}")
                        continue
                    return Explanation(set(foil_model.symbols(shown=True)))
                log.warning("No foil found.")
    raise RuntimeError("No explanation graph found.")
