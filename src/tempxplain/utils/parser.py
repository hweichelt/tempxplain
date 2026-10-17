"""
The command line parser for the project.
"""

from argparse import ArgumentParser
from importlib import metadata
from textwrap import dedent
from typing import Any, cast

from ..backend.server import DEFAULT_FRONTEND_PORT, DEFAULT_HOST, DEFAULT_PORT
from . import logging

__all__ = ["get_parser"]

VERSION = metadata.version("tempxplain")
SYMBOL_STDIN = "-"


def get_parser() -> ArgumentParser:
    """
    Return the parser for command line options.
    """
    parser = ArgumentParser(
        prog="tempxplain",
        description=dedent(
            """\
            tempxplain
            filldescription
            """
        ),
    )
    levels = [
        ("error", logging.ERROR),
        ("warning", logging.WARNING),
        ("info", logging.INFO),
        ("debug", logging.DEBUG),
    ]

    def get(levels: list[tuple[str, int]], name: str) -> int | None:
        for key, val in levels:
            if key == name:
                return val
        return None  # nocoverage

    parser.add_argument(
        "--log",
        default="info",
        choices=[val for _, val in levels],
        metavar=f"{{{','.join(key for key, _ in levels)}}}",
        help="set log level [%(default)s]",
        type=cast(Any, lambda name: get(levels, name)),
    )

    parser.add_argument(
        "files",
        nargs="*",
        metavar="FILE",
        help=f"logic program files to load, {SYMBOL_STDIN} reads from standard input",
    )
    parser.add_argument(
        "-q",
        "--query",
        required=True,
        help="the query that should be satisfied in the foil model. (Follows the tempql syntax)",
    )
    parser.add_argument("--viz", help="visualization encoding for a domain timestep")

    parser.add_argument("--host", default=DEFAULT_HOST, help="address the server listens on [%(default)s]")
    parser.add_argument("--port", default=DEFAULT_PORT, type=int, help="port the server listens on [%(default)s]")
    parser.add_argument(
        "--port-frontend",
        default=DEFAULT_FRONTEND_PORT,
        type=int,
        help="port the frontend is served on, 0 picks some free port [%(default)s]",
    )
    parser.add_argument("--no-frontend", action="store_true", help="only run the backend")
    parser.add_argument("--no-open", action="store_true", help="do not open the frontend in a browser")

    parser.add_argument("--version", "-v", action="version", version=f"%(prog)s {VERSION}")
    return parser
