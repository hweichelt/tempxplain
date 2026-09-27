"""
The backend API.

Functions are exposed by decorating them with `@rpc.method()`. Their return value has to be JSON serializable.
"""

from dataclasses import dataclass

from .rpc import Registry

__all__ = ["ServerState", "rpc"]


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
