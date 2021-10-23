import asyncio
import logging
from os import PathLike
from typing import Optional, List, Coroutine

import requests
import urllib3
from PyTado.interface import Tado
from requests.adapters import HTTPAdapter

from tado_autoassist.assistants import OpenWindowAssistant, GeofencingAssistant
from tado_autoassist.config import settings

BACKOFF_FACTOR = 1.0


async def run_autoassist(
        username: str,
        password: str,
        open_window_interval: Optional[float],
        geofencing_interval: Optional[float],
):
    tado = Tado(
        username=username,
        password=password,
        http_session=create_http_session(),
    )

    coroutines: List[Coroutine] = []

    if open_window_interval is not None:
        coroutines.append(OpenWindowAssistant(tado=tado).run(check_interval=open_window_interval))

    if geofencing_interval is not None:
        coroutines.append(GeofencingAssistant(tado=tado).run(check_interval=geofencing_interval))

    assert len(coroutines) > 0

    await asyncio.gather(*coroutines)


def create_http_session() -> requests.Session:
    # noinspection PyTypeChecker
    retry_strategy = urllib3.Retry(
        total=None,
        backoff_factor=BACKOFF_FACTOR,
    )
    adapter = HTTPAdapter(max_retries=retry_strategy)
    session = requests.Session()
    session.mount('http://', adapter)
    session.mount('https://', adapter)
    return session


def configure_logging(log_file_name: Optional[str | PathLike[str]] = None):
    logging.basicConfig(
        filename=log_file_name,
        level=logging.DEBUG,
        format='%(asctime)s.%(msecs)03d %(levelname)s %(module)s - %(funcName)s: %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S',
    )


if __name__ == '__main__':
    configure_logging(log_file_name=settings.log_file)
    asyncio.run(run_autoassist(
        username=settings.username,
        password=settings.password,
        open_window_interval=settings.open_window_interval,
        geofencing_interval=settings.geofencing_interval,
    ))
