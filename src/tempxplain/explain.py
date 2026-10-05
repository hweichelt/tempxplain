"""Functionality for generating the explanations with asplain."""

from collections.abc import Iterable
from pathlib import Path
from typing import cast

import clingo
from asplain import Foil, construct_program_graph, set_foil_ctl, set_model_subgraphs_ctl
from asplain.transformations.transformers import Transformation, apply_transformation_sequence
from asplain.utils.clingo import get_query_prg, symbols_to_prg
from clingo import SolveHandle, Symbol
from clingo.script import enable_python

from tempxplain.utils.logging import get_logger

from .utils.io import read_file

__all__ = ["explanation_graph"]

log = get_logger("server.explain")

# Enable python for the clingo encodings in asplain using it
enable_python()

DEFAULT_COST_ENCODING = Path(__file__).parent / "encodings" / "cost" / "default.lp"
NUMBER_OF_EXPLANATIONS = 1


def parse_query_program(query: str) -> str:
    """Parse a query to get the query program for asplain."""
    # TODO: Split query into include and exclude here
    query_include: list[Symbol] = []
    query_exclude: list[Symbol] = []
    return get_query_prg(query_include, query_exclude)


def parse_model(model_prg: str) -> set[str]:
    """Parse a model program to get the model's symbol strings."""
    control_model = clingo.Control(["1", "--warn=none"])
    control_model.add(model_prg)
    control_model.ground([("base", [])])
    with control_model.solve(yield_=True) as solve_handle:
        sh = cast(SolveHandle, solve_handle)
        symbols = set()
        for m in sh:
            symbols = {str(s) for s in m.symbols(atoms=True)}
        return symbols


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
            Transformation.INERTIA_CONDENSATION,
        ],
    )


def explanation_graph(
    files: list[str],
    constants: dict[str, str],
    assumptions: set[tuple[str, bool]],
    model_program: str,
    query: str,
) -> set[Symbol]:
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
    model_subgraphs_ctl = set_model_subgraphs_ctl(pg=reference_pg, ctl=control, model_symbols=list(model_symbols))
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

                foil_found = False
                for foil_model in fh:
                    if not foil_model.optimality_proven:
                        log.debug(f"Skipping non-optimal foil model {foil_model.number}")
                        continue
                    foil_found = True
                    explanation_symbols = transform_temporal(list(foil_model.symbols(shown=True)))
                    explanation_graph = symbols_to_prg(explanation_symbols)
                    foil = Foil.from_explanation_graph(explanation_graph)

                    print("FOIL", foil)
                if not foil_found:
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

                foil_found = False
                for foil_model in fh:
                    if not foil_model.optimality_proven:
                        log.info(f"Skipping non-optimal foil model {foil_model.number}")
                        continue
                    foil_found = True
                    explanation_graph = symbols_to_prg(list(foil_model.symbols(shown=True)))
                    explanation_symbols = transform_temporal(list(foil_model.symbols(shown=True)))
                    explanation_graph = symbols_to_prg(explanation_symbols)
                    foil = Foil.from_explanation_graph(explanation_graph)

                    print("FOIL", foil)
                if not foil_found:
                    log.warning("No foil found.")

    return set()
