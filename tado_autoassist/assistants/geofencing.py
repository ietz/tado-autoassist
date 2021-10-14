from tado_autoassist.assistants.assistant import Assistant


class GeofencingAssistant(Assistant):
    def check(self):
        mobile_devices = self._tado.getMobileDevices()
        is_someone_home = any(device['location']['atHome'] for device in mobile_devices)

        if is_someone_home:
            self._tado.setHome()
        else:
            self._tado.setAway()
