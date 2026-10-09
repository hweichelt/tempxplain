"""
The backend API.

Functions are exposed by decorating them with `@rpc.method()`. Their return value has to be JSON serializable.
"""

from typing import Literal

from tempxplain.server import ServerState

from .bindings import Explanation, ProgramData
from .explain import MODEL_STRING_FOIL_TYPE, MODEL_STRING_REF_TYPE, Model
from .rpc import Registry
from .utils.logging import get_logger
from .visualize import visualize_domain

__all__ = ["rpc"]

log = get_logger("tempxplain.api")
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
def get_visualization(state: ServerState, model: MODEL_STRING_REF_TYPE | MODEL_STRING_FOIL_TYPE, t: int) -> str | None:
    """Get the domain visualization of the specified model at time `t` as svg."""
    if state.program_data.viz_file is None:
        return None
    t_start = state.explanation.interval_transformed[0]
    t_end = state.explanation.interval_transformed[1]
    log.info(f"{t}, [{t_start},{t_end}]")
    if not (t_start <= t <= t_end):
        log.warning(f"Cannot generate visualization at t={t} since it is out of bounds [{t_start},{t_end}]")
        return None
    return visualize_domain(state, Model(model), t)


@rpc.method()
def get_program_data(state: ServerState) -> ProgramData:
    """Get data for the input programs."""
    return state.program_data


@rpc.method()
def get_explanation(state: ServerState) -> Explanation:
    """Get details of the logic program."""
    exp = state.explanation
    visualize_domain(state, Model.FOIL, 2)
    return Explanation(
        graph=exp.graph,
        partitions={t: [str(a.symbol) for a in atoms] for t, atoms in exp.partitions_transformed.items()},
        timeframe_full=exp.interval_transformed,
        timeframe_explanation=exp.interval_transformed,
        fluent_matrix={
            str(f): [m.value for m in membership] for f, membership in exp.fluent_matrix_transformed.items()
        },
    )
