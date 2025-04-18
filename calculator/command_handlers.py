"""Module containing the handler functions for CLI commands."""

import logging
import sys

from calculator.server import Server

def calculator() -> None:
    """Handle for running the server for remote calculator."""
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger(__name__)
    logger.info("Running calculator server...")

    server = Server()
    sys.exit(server.main(sys.argv))