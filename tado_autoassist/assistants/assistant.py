import asyncio

from PyTado.interface import Tado


class Assistant:
    def __init__(self, tado: Tado):
        self._tado = tado

    async def run(self, check_interval: float):
        while True:
            self.check()
            await asyncio.sleep(check_interval)

    def check(self):
        raise NotImplementedError()
