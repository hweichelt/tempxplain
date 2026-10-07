"""
The backend API.

Functions are exposed by decorating them with `@rpc.method()`. Their return value has to be JSON serializable.
"""

from dataclasses import dataclass
from typing import Literal

from asplain.utils.viz import viz_graph

from tempxplain.explain import explanation

from .rpc import Registry

__all__ = ["ServerState", "rpc"]


@dataclass
class Explanation:
    """
    Details of the logic program.
    """

    graph: str
    partitions: dict[int, list[str]]
    timeframe_full: tuple[int, int]
    timeframe_explanation: tuple[int, int]
    fluent_matrix: dict[str, list[str]]


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
    exp = explanation(
        files=state.program_data.files,
        constants={},
        assumptions=set(),
        model_program="",
        query=state.query,
    )
    print(f"MATRIX: {exp.fluent_matrix}")
    with open("out/graph.lp", "w") as f:
        f.write(exp.graph)
        viz_graph(
            pg=exp.graph,
            title="Explanation Graph",
            name="contrastive_pg",
        )
    return Explanation(
        graph=exp.graph,
        partitions={t: [str(a.symbol) for a in atoms] for t, atoms in exp.partitions.items()},
        timeframe_full=exp.interval,
        timeframe_explanation=exp.interval,
        fluent_matrix={str(f): [m.value for m in membership] for f, membership in exp.fluent_matrix.items()},
    )
