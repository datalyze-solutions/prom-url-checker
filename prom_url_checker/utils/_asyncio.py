"""Helper functions to work with pythons asyncio functions"""

import signal
from typing import Any, Callable, Dict, List, Optional
from typing import NamedTuple
from typing import overload, TypeVar

from prom_url_checker.exceptions import raise_graceful_exit


def runner_setup(loop) -> None:
    """Adds exit signals to the given asyncio loop on which the app exits gracefully"""
    signals = (
        signal.SIGHUP,
        signal.SIGTERM,
        signal.SIGINT,
        signal.SIGQUIT
    )
    for s in signals:
        loop.add_signal_handler(s, raise_graceful_exit)
