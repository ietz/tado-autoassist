import logging
from dataclasses import dataclass
from typing import Set

from PyTado.interface import Tado

from tado_autoassist.assistants.assistant import Assistant

logger = logging.getLogger(__name__)


class GeofencingAssistant(Assistant):
    def __init__(self, tado: Tado):
        super().__init__(tado=tado)
        self.previously_home_devices: Set[Device] = set()

    def check(self):
        mobile_device_states = self._tado.getMobileDevices()
        home_devices = {
            Device(id=device['id'], name=device['name'])
            for device in mobile_device_states
            if device['location']['atHome']
        }

        log_home_device_changes(home_devices, self.previously_home_devices)

        is_someone_home = len(home_devices) > 0
        was_someone_home = len(self.previously_home_devices) > 0
        if is_someone_home != was_someone_home:
            if is_someone_home:
                logger.info('Switching to home mode')
                self._tado.setHome()
            else:
                logger.info('Switching to away mode')
                self._tado.setAway()

        self.previously_home_devices = home_devices


@dataclass(frozen=True, eq=True)
class Device:
    id: int
    name: str

    def __str__(self):
        return self.name


def log_home_device_changes(now_home: Set[Device], previously_home: Set[Device]):
    home_changes = [
        ('came', now_home - previously_home),
        ('left', previously_home - now_home),
    ]
    for change, change_devices in home_changes:
        if len(change_devices) > 0:
            logger.info(f'{", ".join(device.name for device in change_devices)} {change} home')

