"""Simple HTTP server serving the built frontend."""

import threading
import webbrowser
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from .utils.logging import get_logger

__all__ = ["FRONTEND_DIR", "open_frontend", "start_frontend"]

FRONTEND_DIR = Path(__file__).parent / "frontend"
FRONTEND_DIR_PROJECT = Path(__file__).parent / "frontend/tempxplain"

log = get_logger("frontend")


class _Handler(SimpleHTTPRequestHandler):
    """Serve static files and log requests."""

    def log_message(self, format: str, *args: object) -> None:
        log.debug(format % args)


def start_frontend(host: str, port: int, directory: Path = FRONTEND_DIR) -> ThreadingHTTPServer:
    """
    Serve the built frontend in a background thread.

    The returned server must be closed with `shutdown()` and `server_close()`.
    """
    if not (directory / "index.html").is_file():
        raise FileNotFoundError(f"no built frontend in '{directory}', run 'npm run build' in '{FRONTEND_DIR_PROJECT}'")
    server = ThreadingHTTPServer((host, port), partial(_Handler, directory=str(directory)))
    threading.Thread(target=server.serve_forever, name="frontend", daemon=True).start()
    return server


def open_frontend(frontend_url: str, backend_url: str) -> None:  # nocoverage
    """Open the frontend in the user's default browser."""
    webbrowser.open(f"{frontend_url}?backend={backend_url}")
