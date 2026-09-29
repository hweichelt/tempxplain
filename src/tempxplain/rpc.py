"""
Remote procedure calls over JSON messages.

The frontend sends requests of the form

    `{"id": 1, "method": "name", "params": {"key": "value"}}`

and receives exactly one response per request, either

    `{"id": 1, "result": ...}`

or

    `{"id": 1, "error": {"type": "ErrorName", "message": "..."}}`
"""

import asyncio
import dataclasses
import inspect
import json
from collections.abc import Callable
from typing import Any, Generic, TypeVar

from .utils.logging import get_logger

__all__ = ["Registry", "RpcError"]

State = TypeVar("State")
Handler = TypeVar("Handler", bound=Callable[..., Any])

log = get_logger("rpc")


class RpcError(Exception):
    """An error that is reported back to the frontend."""

    def __init__(self, kind: str, message: str) -> None:
        """Initialize the error with its kind and a message."""
        super().__init__(message)
        self.kind = kind
        self.message = message


def _to_json(value: object) -> object:
    """Convert values that `json` cannot serialize by itself."""
    if dataclasses.is_dataclass(value) and not isinstance(value, type):
        return dataclasses.asdict(value)
    raise TypeError(f"Object of type {type(value).__name__} is not JSON serializable")


class Registry(Generic[State]):
    """
    Functions that can be called by the frontend.

    Each function receives the server state as first argument followed by the parameters of the request as keyword
    arguments.
    """

    def __init__(self) -> None:
        """Initialize an empty registry."""
        self._methods: dict[str, Callable[..., Any]] = {}

    def method(self, name: str | None = None) -> Callable[[Handler], Handler]:
        """Register a function under the given name (default: function name)."""

        def decorator(function: Handler) -> Handler:
            key = function.__name__ if name is None else name  # ty: ignore[unresolved-attribute]
            if key in self._methods:
                raise ValueError(f"Method '{key}' is already registered")
            self._methods[key] = function
            return function

        return decorator

    async def call(self, state: State, name: str, params: dict[str, Any]) -> object:
        """
        Call the method with the given name.

        Coroutine functions are awaited, plain functions run in a worker thread
        so that long running computations do not block the server.
        """
        function = self._methods.get(name)
        if function is None:
            raise RpcError("MethodNotFound", f"unknown method '{name}'")
        try:
            inspect.signature(function).bind(state, **params)
        except TypeError as e:
            raise RpcError("InvalidParams", f"{name}: {e}") from e
        if inspect.iscoroutinefunction(function):
            return await function(state, **params)
        return await asyncio.to_thread(function, state, **params)

    async def handle_request(self, state: State, message: str | bytes) -> str:
        """Process a raw request and return the raw response."""
        request_id = None
        try:
            try:
                request = json.loads(message)
            except ValueError as e:
                raise RpcError("ParseError", f"invalid JSON: {e}") from e
            if not isinstance(request, dict):
                raise RpcError("InvalidRequest", "request must be an object")
            request_id = request.get("id")
            name = request.get("method")
            params = request.get("params", {})
            if not isinstance(name, str):
                raise RpcError("InvalidRequest", "'method' must be a string")
            if not isinstance(params, dict):
                raise RpcError("InvalidRequest", "'params' must be an object")
            try:
                result = await self.call(state, name, params)
                return json.dumps({"id": request_id, "result": result}, default=_to_json)
            except RpcError:
                raise
            except Exception as e:  # pylint: disable=broad-exception-caught
                log.exception(f"method '{name}' failed")
                raise RpcError(type(e).__name__, str(e)) from e
        except RpcError as e:
            return json.dumps({"id": request_id, "error": {"type": e.kind, "message": e.message}})
