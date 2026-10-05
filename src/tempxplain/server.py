"""The WebSocket server connecting to the frontend."""

from contextlib import suppress
from typing import Any

from websockets.asyncio.server import Server, ServerConnection, serve
from websockets.exceptions import ConnectionClosed

from .rpc import Registry
from .utils.logging import get_logger

DEFAULT_HOST = "127.0.0.1"
DEFAULT_PORT = 8765
DEFAULT_FRONTEND_PORT = 8000

log = get_logger("server")


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
