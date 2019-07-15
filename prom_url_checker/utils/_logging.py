"""Helper functions for logging"""

import logging
from typing import Any, Callable, Dict, List, Optional

def logging_setup(logging_level=logging.DEBUG) -> None:
    """Inits the logging system"""
    logging.basicConfig(level=logging_level)

    # Silence asyncio and aiohttp loggers
    logging.getLogger("asyncio").setLevel(logging.ERROR)
    logging.getLogger("aiohttp").setLevel(logging.ERROR)
