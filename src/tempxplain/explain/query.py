"""Functionality for parsing the queries of temporal explanations."""

import clingo
from asplain.utils.logging import get_logger
from clingo import Symbol

QUERY_NEGATION_PREFIX = "-"


log = get_logger("query")


def get_query_prg(query_include: list[Symbol], query_exclude: list[Symbol]) -> str:
    """
    Get the query program string for the given included and excluded query atoms.

    Args:
        query_include: A list of symbols to include in the query.
        query_exclude: A list of symbols to exclude from the query.

    Returns:
        A string representing the query as an ASP program.
    """
    qi = "".join([f"query({str(s)},1)." for s in query_include])
    qe = "".join([f"query({str(s)},0)." for s in query_exclude])
    return qi + qe


def parse_query_program(query: str) -> str:
    """Parse a query to get the query program for asplain."""
    query_include: list[Symbol] = []
    query_exclude: list[Symbol] = []
    for literal in query.strip().split():
        if literal.startswith(QUERY_NEGATION_PREFIX):
            query_exclude.append(clingo.parse_term(literal.removeprefix(QUERY_NEGATION_PREFIX)))
        else:
            query_include.append(clingo.parse_term(literal))

    query_program = get_query_prg(query_include, query_exclude)
    log.info(f"Query program: {query_program}")
    return query_program
