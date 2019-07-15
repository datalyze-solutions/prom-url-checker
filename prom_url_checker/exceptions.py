"""Exceptions for the prom_url_checker package
Custom exceptions used by prom_url_checker for more helpful error messages
"""


class GracefulExit(SystemExit):
    """Exception to gracefully tear down the asyncio app"""
    code = 1


def raise_graceful_exit() -> None:
    """Raises a GracefulExit exception"""
    raise GracefulExit()
