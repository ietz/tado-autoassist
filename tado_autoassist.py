import asyncio
from typing import Dict

from PyTado.interface import Tado


async def main():
    tado = Tado(username='username', password='password')
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


if __name__ == '__main__':
    asyncio.run(main())
