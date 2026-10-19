"""The WebSocket server connecting to the frontend."""

from collections.abc import Generator
from contextlib import suppress
from typing import Any, cast

from websockets.asyncio.server import Server, ServerConnection, serve
from websockets.exceptions import ConnectionClosed

from ..explain import Explanation, ModelGraph, navigate_foil_models, navigate_reference_models
from ..utils.logging import get_logger
from .bindings import ProgramData
from .rpc import Registry

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765
DEFAULT_FRONTEND_PORT = 8000
PATH_EXPLANATION_GRAPH = "out/graph"


log = get_logger("server")


class ServerState:
    """
    State of the backend server.
    """

    def __init__(self, program_data: ProgramData, query: str | None = None) -> None:
        """Initialize the server state with the given program data."""
        self.program_data = program_data
        self._query: str | None = query
        self._current_reference_id: int | None = None
        self._current_explanation_id: tuple[int, int] | None = None
        self._references: dict[int, ModelGraph] = {}
        self._explanations: dict[tuple[int, int], Explanation] = {}
        self._generator_foil: Generator[Explanation] | None = None
        self._generator_reference: Generator[ModelGraph] = navigate_reference_models(
            files=self.program_data.files,
            constants={},
            assumptions=set(),
            model_program="",
        )

        self.next_reference()

    @property
    def current_reference(self) -> tuple[int, ModelGraph] | None:
        """Return the current reference model with its ID."""
        if self._current_reference_id is None:
            return None
        return self._current_reference_id, self._references[self._current_reference_id]

    @property
    def current_explanation(self) -> tuple[tuple[int, int], Explanation] | None:
        """Return the current explanation with its ID."""
        if self._current_explanation_id is None:
            return None
        return self._current_explanation_id, self._explanations[self._current_explanation_id]

    def get_explanation(self, ref_id: int, foil_id: int) -> Explanation:
        """Explain the provided reference model with it's proivded foil counterpart."""
        return self._explanations[(ref_id, foil_id)]

    def next_reference(self) -> None:
        """Find the next reference model."""
        try:
            model = next(self._generator_reference)
            model_id = 1 if self._current_reference_id is None else self._current_reference_id + 1
            self._references[model_id] = model
            self._current_reference_id = model_id
        except StopIteration:
            log.error("Reference models exhausted")

    def next_explanation(self) -> bool:
        """Find the next explanation."""
        if self._generator_foil is None:
            if self._current_reference_id is None:
                raise RuntimeError("No reference model available to explain")
            if self._query is None:
                raise RuntimeError("No query available to explain")
            self._generator_foil = navigate_foil_models(
                files=self.program_data.files,
                constants={},
                assumptions=set(),
                reference_model=self._references[self._current_reference_id],
                query=self._query,
            )
        try:
            exp = next(self._generator_foil)
            exp_id = (
                (1, 1)
                if self._current_explanation_id is None
                else (cast(int, self._current_reference_id), self._current_explanation_id[1] + 1)
            )
            self._explanations[exp_id] = exp
            self._current_explanation_id = exp_id
            return True
        except StopIteration:
            log.error("Foil models exhausted")
            return False


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
