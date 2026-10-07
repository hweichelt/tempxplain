"""
The backend API.

Functions are exposed by decorating them with `@rpc.method()`. Their return value has to be JSON serializable.
"""

from dataclasses import dataclass
from typing import Literal

from tempxplain.explain import explanation_graph

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
class ProgramData:
    files: list[str]


@dataclass
class ServerState:
    """
    State of the backend server.
    """

    program_data: ProgramData
    query: str
    program: str = ""


rpc: Registry[ServerState] = Registry()


@rpc.method()
def ping(_state: ServerState) -> Literal["pong"]:
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
def get_program_data(state: ServerState) -> ProgramData:
    """Get data for the input programs."""
    return state.program_data


@rpc.method()
def get_explanation(state: ServerState) -> Explanation:
    """Get details of the logic program."""
    eg = explanation_graph(
        files=state.program_data.files,
        constants={},
        assumptions=set(),
        model_program="",
        query=state.query,
    )
    return Explanation(
        graph="",
        partitions=[],
        timeframe_full=(0, 10),
        timeframe_explanation=(2, 8),
    )
