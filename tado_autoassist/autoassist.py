import asyncio

import requests
import urllib3
from PyTado.interface import Tado
from requests.adapters import HTTPAdapter

from tado_autoassist.assistants import OpenWindowAssistant, GeofencingAssistant

BACKOFF_FACTOR = 1.0


async def run_autoassist():
    tado = Tado(
        username='username',
        password='password',
        http_session=create_http_session(),
    )
    await asyncio.gather(
        OpenWindowAssistant(tado=tado).run(check_interval=10.0),
        GeofencingAssistant(tado=tado).run(check_interval=60.0),
    )


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


if __name__ == '__main__':
    asyncio.run(run_autoassist())
