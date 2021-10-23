import asyncio
from typing import Optional, List, Coroutine

import requests
import urllib3
from PyTado.interface import Tado
from requests.adapters import HTTPAdapter

from tado_autoassist.assistants import OpenWindowAssistant, GeofencingAssistant

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
