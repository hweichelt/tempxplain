"""Temporal functionality and helpers for the backend."""

from enum import Enum

from clingo import Symbol

PREDICATE_SIGNATURE_ACTION = ("occurs", 2)
PREDICATE_SIGNATURE_FLUENT = ("holds", 2)


class AtomType(Enum):
    """Temporal type of an atom."""

    STATIC = "Static"
    TIMED = "Timed"


def is_action(atom: Symbol) -> bool:
    """Check if an atom is an action."""
    return atom.match(*PREDICATE_SIGNATURE_ACTION)


def is_fluent(atom: Symbol) -> bool:
    """Check if an atom is a fluent."""
    return atom.match(*PREDICATE_SIGNATURE_FLUENT)


def atom_type(atom: Symbol) -> AtomType:
    """Determine the temporal type of an atom."""
    if is_action(atom) or is_fluent(atom):
        return AtomType.TIMED
    return AtomType.STATIC


def atom_time(atom: Symbol) -> int | None:
    """Extract the time from a timed atom."""
    match atom_type(atom):
        case AtomType.TIMED:
            return atom.arguments[1].number
        case AtomType.STATIC:
            return None


def atom_base(atom: Symbol) -> Symbol:
    """Extract the base atom from a timed atom."""
    match atom_type(atom):
        case AtomType.TIMED:
            return atom.arguments[0]
        case AtomType.STATIC:
            return atom
