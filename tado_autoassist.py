import asyncio
from typing import Dict

import requests
import urllib3
from PyTado.interface import Tado
from requests.adapters import HTTPAdapter

BACKOFF_FACTOR = 1.0


async def main():
    tado = Tado(
        username='username',
        password='password',
        http_session=create_http_session(),
    )
    await OpenWindowAssistant(tado=tado).run(check_interval=10.0)


class OpenWindowAssistant:
    def __init__(self, tado: Tado):
        self._tado = tado

    async def run(self, check_interval: float):
        while True:
            self.check()
            await asyncio.sleep(check_interval)

    def check(self):
        zone_states: Dict[int, Dict] = {int(id_): state for id_, state in self._tado.getZoneStates()['zoneStates'].items()}

        for zone_id, zone in zone_states.items():
            if zone.get('openWindowDetected', False):
                self._tado.setOpenWindow(zone_id)


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
    asyncio.run(main())
