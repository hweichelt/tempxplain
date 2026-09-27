"""
The main entry point for the application.
"""

import asyncio
import sys

from .api import ServerState, rpc
from .server import run_server
from .utils.logging import configure_logging, get_logger
from .utils.parser import get_parser


def main() -> None:
    """
    Run the main function.
    """
    parser = get_parser()
    args = parser.parse_args()
    configure_logging(sys.stderr, args.log, sys.stderr.isatty())

    log = get_logger("main")
    try:
        asyncio.run(run_server(rpc, ServerState(), args.host, args.port))
    except KeyboardInterrupt:
        log.info("server stopped")


if __name__ == "__main__":
    main()
