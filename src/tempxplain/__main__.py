"""
The main entry point for the application.
"""

import asyncio
import sys
from logging import Logger

from .backend.api import ProgramData, ServerState, rpc
from .backend.server import run_server
from .frontend import open_frontend, start_frontend
from .utils.logging import configure_logging, get_logger
from .utils.parser import get_parser


def backend_url(host: str, port: int) -> str:
    """Construct the backend url string."""
    return f"ws://{host}:{port}"


def frontend_url(host: str, port: int) -> str:
    """Construct the frontend url string."""
    return f"http://{host}:{port}"


def run_backend(
    host: str,
    port: int,
    log: Logger,
    files: list[str],
    query: str | None,
    cost_file: str | None,
    viz_file: str | None,
    model_file: str | None,
) -> None:
    """Start the backend in an async environment."""
    try:
        data = ProgramData(
            files=files,
            viz_file=viz_file,
            cost_file=cost_file,
            model_file=model_file,
        )
        state = ServerState(data, query=query)
        asyncio.run(run_server(rpc, state, host, port))
    except KeyboardInterrupt:
        log.info("server stopped")


def run_frontend(
    host: str,
    port: int,
    backend_url: str,
    log: Logger,
    open: bool = True,
) -> None:
    """Serve the frontend in the background and open it in the browser."""
    server = start_frontend(host, port)
    url_frontend = frontend_url(host, server.server_port)
    log.info(f"Frontend available at {url_frontend}")
    if open:
        open_frontend(url_frontend, backend_url)


def main() -> None:
    """Run the main function."""
    parser = get_parser()
    args = parser.parse_args()
    configure_logging(sys.stderr, args.log, sys.stderr.isatty())

    log = get_logger("main")
    if len(args.files) == 0:
        log.error("No program files provided.")
        raise ValueError("tempxplain cannot be started without a program to explain.")
    if not args.no_frontend:
        run_frontend(args.host, args.port_frontend, backend_url(args.host, args.port), log, not args.no_open)

    run_backend(
        args.host,
        args.port,
        log,
        query=args.query,
        files=args.files,
        viz_file=args.viz,
        cost_file=args.cost_file,
        model_file=args.model_file,
    )


if __name__ == "__main__":
    main()
