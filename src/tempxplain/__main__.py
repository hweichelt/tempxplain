"""
The main entry point for the application.
"""

import asyncio
import sys
from logging import Logger

from .api import ServerState, rpc
from .server import run_server
from .utils.logging import configure_logging, get_logger
from .utils.parser import get_parser


def run_backend(
    host: str,
    port: int,
    log: Logger,
) -> None:
    """Start the backend in an async environment."""
    try:
        asyncio.run(run_server(rpc, ServerState(), host, port))
    except KeyboardInterrupt:
        log.info("server stopped")


def main() -> None:
    """
    Run the main function.
    """
    parser = get_parser()
    args = parser.parse_args()
    configure_logging(sys.stderr, args.log, sys.stderr.isatty())

    log = get_logger("main")
    run_backend(args.host, args.port, log)


if __name__ == "__main__":
    main()
