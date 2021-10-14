from typing import Dict

from tado_autoassist.assistants.assistant import Assistant


class OpenWindowAssistant(Assistant):
    def check(self):
        zone_states: Dict[int, Dict] = {int(id_): state for id_, state in self._tado.getZoneStates()['zoneStates'].items()}

        for zone_id, zone in zone_states.items():
            if zone.get('openWindowDetected', False):
                self._tado.setOpenWindow(zone_id)
