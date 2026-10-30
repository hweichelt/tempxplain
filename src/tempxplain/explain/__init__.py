"""Functionality for generating the explanations with asplain."""

from collections.abc import Generator, Iterable
from dataclasses import dataclass
from enum import Enum
from functools import cached_property
from pathlib import Path
from typing import Literal, cast, get_args

import clingo
from asplain import construct_program_graph, set_foil_ctl, set_model_subgraphs_ctl
from asplain.transformations.transformers import Transformation, apply_transformation_sequence
from asplain.utils.clingo import symbols_to_prg
from clingo import SolveHandle, Symbol
from clingo.script import enable_python

from tempxplain.explain.query import parse_query_program

from ..utils.io import read_file
from ..utils.logging import get_logger
from ..utils.symbols import parse_model, to_program
from .graph import TemporalExplanationGraph
from .temporal import AtomType, atom_base, atom_time, atom_type, is_action, is_fluent

log = get_logger("server.explain")

# Enable python for the clingo encodings in asplain using it
enable_python()

DEFAULT_DYNAMIC_TAGS_ENCODING = Path(__file__).parent.parent / "encodings" / "tags" / "default.lp"
DEFAULT_COST_ENCODING = Path(__file__).parent.parent / "encodings" / "cost" / "default.lp"
NUMBER_OF_REFERENCE_MODELS = 0
NUMBER_OF_EXPLANATIONS = 0
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
class ModelGraph:
    """Representation of an explanation model."""

    symbols: set[Symbol]

    @cached_property
    def program(self) -> str:
        """The explanation graph as a program string."""
        return to_program(self.symbols)

    @cached_property
    def atoms(self) -> set[Atom]:
        """The atoms of the explanation graph with assigned model memberships."""
        return ModelGraph._explanation_symbols_to_atoms(self.symbols)

    @cached_property
    def atoms_static(self) -> set[Atom]:
        """The static atoms of the explanation graph."""
        return {a for a in self.atoms if a.time is None}

    @cached_property
    def atoms_timed(self) -> set[Atom]:
        """The timed atoms of the explanation graph."""
        return {a for a in self.atoms if a.time is not None}

    @cached_property
    def fluents(self) -> set[Atom]:
        """The fluent atoms of the explanation graph."""
        return {a for a in self.atoms_timed if a.is_fluent}

    @cached_property
    def partitions(self) -> dict[int, set[Atom]]:
        """The partitions of the explanation graph, indexed by timepoint."""
        partitions: dict[int, set[Atom]] = {}
        for atom in self.atoms_timed:
            if (timepoint := atom.time) is not None:
                partitions.setdefault(timepoint, set()).add(atom)
        return partitions

    @cached_property
    def interval(self) -> tuple[int, int]:
        """The time interval of the explanation graph as a tuple (start, end)."""
        return min(self.partitions), max(self.partitions)

    @cached_property
    def length(self) -> int:
        """The length of the explanation graph (the number of timepoints)."""
        return self.interval[1] - self.interval[0] + 1

    @cached_property
    def fluent_matrix(self) -> dict[Symbol, list[ModelMembership]]:
        """`Symbol` <-> `ModelMembership` matrix for fluents in the explanation graph."""
        return self._fluent_matrix(self.fluents, self.length)

    @staticmethod
    def _fluent_matrix(fluents: set[Atom], length: int) -> dict[Symbol, list[ModelMembership]]:
        """`Symbol` <-> `ModelMembership` matrix for fluents in the explanation graph."""
        fluent_bases = {a.base for a in fluents}
        matrix = {a: [ModelMembership.NONE] * length for a in fluent_bases}
        for atom in fluents:
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
        if t not in range(self.interval[0], self.interval[1] + 1):
            raise ValueError(f"Time {t} is out of range for the explanation interval {self.interval}")
        atoms_model_partition_t = {a.base for a in self.partitions[t] if a.membership.has(model)}
        atoms_static = {a.base for a in self.atoms_static}
        atoms_t = atoms_model_partition_t.union(atoms_static)
        log.info(f"Model state at t={t}: {[str(a) for a in atoms_t]}")
        return atoms_t


@dataclass(frozen=True)
class Explanation:
    """Representation of an explanation graph."""

    full: ModelGraph
    transformed: ModelGraph

    @classmethod
    def from_symbols(cls, symbols: set[Symbol]) -> "Explanation":
        """Create an explanation graph from a set of symbols."""
        return cls(
            ModelGraph(set(symbols)),
            ModelGraph(set(transform_temporal(symbols))),
        )

    @cached_property
    def graph(self) -> TemporalExplanationGraph:
        """The explanation graph."""
        return TemporalExplanationGraph.from_symbols(self.transformed.symbols)


def transform_temporal(symbols: Iterable[Symbol]) -> list[Symbol]:
    """Transform the symbols of an explanation graph with the temporal pruning pipeline."""
    log.info("Applying temporal pruning")
    return apply_transformation_sequence(
        symbols,
        [
            Transformation.NO_MODEL,
            Transformation.FACT_RULES,
            Transformation.STATIC_DOMAIN_FACTS,
            Transformation.LEAF_RULES,
            Transformation.IRRELEVANT,
        ],
    )


def navigate_reference_models(
    files: list[str],
    constants: dict[str, str],
    assumptions: set[tuple[str, bool]],
    model_program: str,
) -> Generator[ModelGraph]:
    """Yield reference models for the given program."""
    model_symbols = parse_model(model_program)
    control = clingo.Control([str(NUMBER_OF_REFERENCE_MODELS), "--warn=none"])
    reference_pg = construct_program_graph(
        list(files),
        constants=constants,
        assumptions=list(assumptions),
        dynamic_tags_files=[str(DEFAULT_DYNAMIC_TAGS_ENCODING)],
    )
    model_subgraphs_ctl = set_model_subgraphs_ctl(pg=reference_pg, ctl=control, model_symbols=model_symbols)
    with model_subgraphs_ctl.solve(yield_=True) as solve_handle:
        sh = cast(SolveHandle, solve_handle)
        found_any = False
        for model in sh:
            found_any = True
            yield ModelGraph(set(model.symbols(atoms=True)))
        if not found_any:
            return None


def find_foil(
    program_graph: str,
    query_program: str,
    cost_program: str,
    number_of_foils: int = NUMBER_OF_EXPLANATIONS,
) -> Generator[Explanation]:
    """Find a single foil explanation for the given program graph, query program, and cost program."""
    control = set_foil_ctl(
        pg=program_graph,
        query_prg=query_program,
        cost_prg=cost_program,
        number_of_foils=number_of_foils,
    )
    with control.solve(yield_=True) as foil_handle:
        sh = cast(SolveHandle, foil_handle)

        for model in sh:
            if not model.optimality_proven:
                log.info(f"Skipping non-optimal foil model {model.number}")
                continue
            yield Explanation.from_symbols(set(model.symbols(shown=True)))
        log.warning("No foil found.")


def navigate_foil_models(
    files: list[str],
    constants: dict[str, str],
    assumptions: set[tuple[str, bool]],
    reference_model: ModelGraph | None,
    query: str,
    custom_cost: str | None = None,
) -> Generator[Explanation]:
    """Compute the explanation graph for a given program with query."""
    query_prg = parse_query_program(query)
    cost_file = Path(custom_cost) if custom_cost is not None else DEFAULT_COST_ENCODING
    cost_prg = read_file(cost_file)
    reference_pg = construct_program_graph(
        list(files),
        constants=constants,
        assumptions=list(assumptions),
        dynamic_tags_files=[str(DEFAULT_DYNAMIC_TAGS_ENCODING)],
    )

    found_any = False
    if reference_model is not None:
        reference_model_pg = symbols_to_prg(list(reference_model.symbols))
        for exp in find_foil(reference_model_pg, query_prg, cost_prg):
            found_any = True
            yield exp

    else:
        log.warning("UNSATISFIABLE. Will proceed to explain.")
        for exp in find_foil(reference_pg, query_prg, cost_prg):
            found_any = True
            yield exp

    if not found_any:
        raise RuntimeError("No explanation graph found.")
