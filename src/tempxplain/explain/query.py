"""Functionality for parsing the queries of temporal explanations."""

from collections.abc import Iterable

from asplain.utils.logging import get_logger
from clingo import Symbol
from tempql.parser import parse
from tempql.semantics import semantics
from tempql.utils import to_symbol

log = get_logger("query")

RULES_TEMPORAL_QUERY_FOIL_FINDING = """
__disable_default_queries__.

% Classify temporal queries
temporal(temporal(Q,T)) :- query(temporal(Q,T),_).

% Normal queries
:- query(A,0), not temporal(A), model(A, foil).
:- query(A,1), not temporal(A), not model(A, foil).

% Temporal queries
:- query(temporal(Q,T),0), holds(Q,T).
:- query(temporal(Q,T),1), not holds(Q,T).
"""


def to_program(query_symbols: Iterable[Symbol]) -> str:
    """Convert the given query symbols to an ASP program string."""
    query_string = " ".join(f"{q}." for q in query_symbols)
    semantics_string = semantics()
    program = f"{semantics_string}\n{query_string}\n{RULES_TEMPORAL_QUERY_FOIL_FINDING}"
    return program


def parse_query_program(query_raw: str) -> str:
    """Parse a tempql query to get the query program for asplain."""
    queries = parse(query_raw)
    query_symbols = [to_symbol(q) for q in queries]
    query_program = to_program(query_symbols)
    log.info(f"Query program: {query_program}")
    return query_program
