"""Main functions for the prom-url-checker"""

import aiohttp
from aiohttp.client_exceptions import ClientConnectorError
from aioprometheus import Counter, Gauge, Histogram, Service, Summary, formats, timer, inprogress, count_exceptions
import asyncio
from collections import namedtuple
import logging
import os
import socket
from typing import Any, Callable, Dict, List, Optional, Type


url_health_result = namedtuple('UrlHealthResult', ['url', 'status'])

const_labels = {
    "host": socket.gethostname(),
    "app": "url_health_checker"
    # "app": f"{__file__}-{uuid.uuid4().hex}",
}
url_request_times = Summary("url_health_request_processing_seconds",
                            "Time spent processing request",
                            const_labels=const_labels)
url_health_metric = Gauge("url_health",
                          "Health status of a url.",
                          const_labels=const_labels)
url_requests_in_progress = Gauge("request_in_progress",
                                 "Number of requests in progress",
                                 const_labels=const_labels)


def urls_from_env(env: str = 'URLS') -> str:
    """Returns the urls string define by a environment variable"""
    try:
        return os.environ[env]
    except KeyError as err:
        raise ValueError(
            f"No environment variable {env} set.\nOriginal error: {err}")


def parse_urls(
    urls: str,
    seperator: str = ','
) -> List[str]:
    """Parses the given urls string with the seperator"""
    return urls.split(seperator)


def parsed_urls(
    urls: str = None,
    fallback: Callable[[str], str] = urls_from_env,
    parser: Callable[[str], List[str]] = parse_urls
) -> List[str]:
    """Function to return the parsed list of urls"""
    if not urls:
        urls = fallback()
    return parser(urls)


@inprogress(url_requests_in_progress, {"route": "/"})
@timer(url_request_times)
async def url_health_check(url: str) -> int:
    """Performs the url check using a HTTP HEAD request and returns the status code"""

    logger = logging.getLogger(__name__)

    try:
        async with aiohttp.ClientSession() as session:
            async with session.head(url) as response:
                logger.debug((url, response.status))
                return url_health_result(url, response.status)
    except ClientConnectorError as err:
        # maybe wrong dns, e.g. a local host only domain not reachable from the container
        logger.error(err)
        return url_health_result(url, 1000)


async def url_checker(gauge: Type[Gauge],
                      url: str,
                      sleeptime: int = 60):
    """Starts an url checker and updates the given gauge periodically"""

    logger = logging.getLogger(__name__)

    while True:
        logger.debug(f"starting next check of {url}")

        result = await url_health_check(url)
        gauge.set({"url": result.url}, result.status)
        await asyncio.sleep(sleeptime)


async def run_server(host: str = "127.0.0.1",
                     port: str = "9999",
                     sleeptime: int = 5,
                     urls: List[str] = None):
    """Starts the metrics server"""
    logger = logging.getLogger(__name__)

    prom_service = Service()
    for metric in (url_request_times, url_health_metric, url_requests_in_progress):
        prom_service.register(metric)

    urls = parsed_urls(urls)
    logger.info(f"Urls to check: {urls}")

    try:
        logger.info('Starting metrics server')
        await prom_service.start(addr=host, port=port)

        url_tasks = [
            url_checker(url_health_metric, url, sleeptime=sleeptime)
            for url in urls
        ]
        tasks = [
            *url_tasks
            # add other tasks if needed
        ]
        await asyncio.gather(*tasks)
    finally:
        await prom_service.stop()
