import logging
from typing import Dict

from PyTado.interface import Tado

from tado_autoassist.assistants.assistant import Assistant

logger = logging.getLogger(__name__)


class OpenWindowAssistant(Assistant):
    def __init__(self, tado: Tado):
        super().__init__(tado=tado)
        self._zones_cache: Dict[int, Dict] = {}

    def check(self):
        zone_states: Dict[int, Dict] = {int(id_): state for id_, state in self._tado.getZoneStates()['zoneStates'].items()}

        for zone_id, zone_state in zone_states.items():
            if zone_state.get('openWindowDetected', False):
                self._tado.setOpenWindow(zone_id)

                zone = self._get_zone(zone_id)
                logger.info(f'Detected an open window in {zone["name"]}. Enabling open window mode.')

    def _get_zone(self, zone_id: int) -> Dict:
        """Get zone metadata (not state) from cache if available"""
        if zone_id not in self._zones_cache:
            self._zones_cache = {zone['id']: zone for zone in self._tado.getZones()}

        return self._zones_cache[zone_id]

