"""Utility functions for working with clingo symbols."""

from collections.abc import Iterable

from clingo import Symbol


def to_program(symbols: Iterable[Symbol]) -> str:
    """Convert a collection of clingo symbols to a program string."""
    return "\n".join(f"{str(symbol)}." for symbol in symbols)
