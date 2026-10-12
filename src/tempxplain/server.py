"""The WebSocket server connecting to the frontend."""

from contextlib import suppress
from dataclasses import dataclass
from functools import cached_property
from typing import Any

from asplain.utils.viz import viz_graph
from websockets.asyncio.server import Server, ServerConnection, serve
from websockets.exceptions import ConnectionClosed

from .bindings import ProgramData
from .explain import Explanation, explanation
from .rpc import Registry
from .utils.logging import get_logger

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765
DEFAULT_FRONTEND_PORT = 8000
PATH_EXPLANATION_GRAPH = "out/graph"


log = get_logger("server")


@dataclass
class ServerState:
    """
    State of the backend server.
    """

    program_data: ProgramData
    query: str
    program: str = ""

    @cached_property
    def explanation(self) -> Explanation:
        """The explanation for the provided program and query."""
        exp = explanation(
            files=self.program_data.files,
            constants={},
            assumptions=set(),
            model_program="",
            query=self.query,
        )
        log.info(f"Writing explanation graph to disk: {PATH_EXPLANATION_GRAPH}")
        with open(f"{PATH_EXPLANATION_GRAPH}.lp", "w") as f:
            f.write(exp.program)
        viz_graph(
            pg=exp.program,
            title="Explanation Graph",
            name=f"{PATH_EXPLANATION_GRAPH}.lp",
        )
        return exp


async def start_server(registry: Registry[Any], state: object, host: str, port: int) -> Server:
    """Start a server with a given API registry."""

    async def handle_connection(connection: ServerConnection) -> None:
        log.info(f"Frontend connected: {connection.remote_address}")
        with suppress(ConnectionClosed):
            async for message in connection:
                await connection.send(await registry.handle_request(state, message))
        log.info(f"Frontend disconnected: {connection.remote_address}")

    return await serve(handle_connection, host, port)


async def run_server(registry: Registry[Any], state: object, host: str, port: int) -> None:  # nocoverage
    """Run the server until the task is cancelled."""
    async with await start_server(registry, state, host, port) as server:
        log.info(f"Listening on ws://{host}:{port}")
        log.info(f"ServerState: {state}")
        await server.serve_forever()
