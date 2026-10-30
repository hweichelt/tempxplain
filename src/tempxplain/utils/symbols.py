"""Utility functions for working with clingo symbols."""

from collections.abc import Iterable
from pathlib import Path
from typing import cast

import clingo
from clingo import SolveHandle, Symbol

from tempxplain.utils.io import read_file


def to_program(symbols: Iterable[Symbol]) -> str:
    """Convert a collection of clingo symbols to a program string."""
    return "\n".join(f"{str(symbol)}." for symbol in symbols)


def parse_model(model_prg: str) -> list[str] | None:
    """Parse a model program to get the model's symbol strings."""
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


def model_program_to_assumptions(model_file: str | None) -> set[tuple[str, bool]]:
    """Convert a model program to a set of assumptions."""
    if model_file is None:
        return set()
    atoms = parse_model(read_file(Path(model_file)))
    if atoms is None:
        return set()
    return {(atom, True) for atom in atoms}
