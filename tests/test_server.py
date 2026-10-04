"""
Test cases for the communication with the frontend.
"""

import json
from dataclasses import dataclass
from typing import Any
from unittest import IsolatedAsyncioTestCase

from websockets.asyncio.client import connect

from tempxplain.api import ServerState, rpc
from tempxplain.rpc import Registry
from tempxplain.server import start_server


class TestRpc(IsolatedAsyncioTestCase):
    """
    Test cases for calling registered methods.
    """

    async def request(self, registry: Registry[Any], state: object, request: object) -> dict[str, Any]:
        """
        Send a request to the registry and return the decoded response.
        """
        return json.loads(await registry.handle_request(state, json.dumps(request)))

    async def test_call(self) -> None:
        """
        Test calling plain and coroutine functions.
        """
        registry: Registry[list[int]] = Registry()

        @registry.method()
        def add(state: list[int], value: int) -> list[int]:
            state.append(value)
            return state

        @registry.method("total")
        async def compute_total(state: list[int]) -> int:
            return sum(state)

        @dataclass
        class Stats:
            values: list[int]

        @registry.method()
        def stats(state: list[int]) -> Stats:
            return Stats(values=state)

        state: list[int] = [1]
        self.assertEqual(
            await self.request(registry, state, {"id": 1, "method": "add", "params": {"value": 2}}),
            {"id": 1, "result": [1, 2]},
        )
        self.assertEqual(await self.request(registry, state, {"id": 2, "method": "total"}), {"id": 2, "result": 3})
        self.assertEqual(
            await self.request(registry, state, {"id": 3, "method": "stats"}), {"id": 3, "result": {"values": [1, 2]}}
        )

        with self.assertRaises(ValueError):
            registry.method("add")(add)

    async def test_errors(self) -> None:
        """
        Test that errors are reported to the frontend.
        """
        registry: Registry[None] = Registry()

        @registry.method()
        def fail(_state: None) -> None:
            raise RuntimeError("failed")

        def error(response: dict[str, Any]) -> str:
            return response["error"]["type"]

        self.assertEqual(error(json.loads(await registry.handle_request(None, "{"))), "ParseError")
        self.assertEqual(error(await self.request(registry, None, [])), "InvalidRequest")
        self.assertEqual(error(await self.request(registry, None, {"id": 1})), "InvalidRequest")
        self.assertEqual(
            error(await self.request(registry, None, {"id": 1, "method": "fail", "params": []})), "InvalidRequest"
        )
        self.assertEqual(error(await self.request(registry, None, {"id": 1, "method": "unknown"})), "MethodNotFound")
        self.assertEqual(
            error(await self.request(registry, None, {"id": 1, "method": "fail", "params": {"x": 1}})), "InvalidParams"
        )
        with self.assertLogs("rpc", "ERROR"):
            response = await self.request(registry, None, {"id": 7, "method": "fail"})
        self.assertEqual(response, {"id": 7, "error": {"type": "RuntimeError", "message": "failed"}})


class TestServer(IsolatedAsyncioTestCase):
    """
    Test cases for the WebSocket server.
    """

    async def test_api(self) -> None:
        """
        Test calling the api over a WebSocket.
        """
        state = ServerState()
        async with await start_server(rpc, state, "127.0.0.1", 0) as server:
            port = next(iter(server.sockets)).getsockname()[1]
            async with connect(f"ws://127.0.0.1:{port}") as connection:

                async def call(request_id: int, method: str, **params: object) -> dict[str, Any]:
                    await connection.send(json.dumps({"id": request_id, "method": method, "params": params}))
                    return json.loads(await connection.recv())

                self.assertEqual(await call(1, "ping"), {"id": 1, "result": "pong"})
                self.assertEqual(await call(2, "set_program", program="a."), {"id": 2, "result": None})
                self.assertEqual(await call(3, "get_program"), {"id": 3, "result": "a."})
                self.assertEqual((await call(4, "get_explanation"))["result"]["timeframe_full"], [0, 10])
        self.assertEqual(state.program, "a.")
