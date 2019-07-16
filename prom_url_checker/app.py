"""Entrypoint for the prom_url_checker"""

import asyncio
import clize
import logging
from prom_url_checker.utils import (
    _logging,
    _asyncio
)
from prom_url_checker.utils import server as prom_server
from typing import Any, Callable, Dict, List, Optional, Type


def run_app(*,
            host: str = "127.0.0.1",
            port: str = "9999",
            sleeptime: (int, 's') = 5,
            urls: str = None,
            debug: (bool, 'd') = False) -> None:
    """Starts the prometheus-url-checker metrics server

    :param host: Host ip to serve on.
    :param port: Port to use
    :param sleeptime: Sleeptime during checks
    :param urls: Comma seperated list of urls to check, e.g. `--urls https://test.domain.de,http://domain.de`.
        If unset, the environment variable `URLS` will be used instead.
    :param debug: Enable debugging mode
    """
    _logging.logging_setup(logging.DEBUG if debug else logging.INFO)
    logger = logging.getLogger(__name__)

    loop = asyncio.get_event_loop()
    logger.debug(f"Settings: {locals()}")

    try:
        _asyncio.runner_setup(loop)
        loop.run_until_complete(
            prom_server.run_server(host=host, port=port, sleeptime=sleeptime, urls=urls))
    finally:
        logger.info('Shutting down metrics server.')


def cli_run() -> None:
    clize.run(run_app)


if __name__ == "__main__":
    cli_run()
