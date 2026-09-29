"""
The backend API.

Functions are exposed by decorating them with `@rpc.method()`. Their return value has to be JSON serializable.
"""

import time
from dataclasses import dataclass

from .rpc import Registry

__all__ = ["ServerState", "rpc"]


@dataclass
class Explanation:
    """
    Details of the logic program.
    """

    graph: str
    partitions: list[str]
    timeframe_full: tuple[int, int]
    timeframe_explanation: tuple[int, int]


@dataclass
class ServerState:
    """
    State of the backend server.
    """

    program: str = ""


rpc: Registry[ServerState] = Registry()


@rpc.method()
def ping(_state: ServerState) -> str:
    """Check that the backend is online and reachable."""
    return "pong"


@rpc.method()
def set_program(state: ServerState, program: str) -> None:
    """Set the logic program."""
    state.program = program


@rpc.method()
def get_program(state: ServerState) -> str:
    """Get the logic program."""
    return state.program


@rpc.method()
def get_explanation(state: ServerState) -> Explanation:
    """Get details of the logic program."""
    return Explanation(
        graph="",
        partitions=[],
        timeframe_full=(0, 10),
        timeframe_explanation=(2, 8),
    )
