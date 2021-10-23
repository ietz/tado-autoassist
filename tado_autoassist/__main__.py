import asyncio

from tado_autoassist.autoassist import run_autoassist
from tado_autoassist.config import settings
from tado_autoassist.logging import configure_logging

configure_logging(log_file_name=settings.get('log_file', None))
asyncio.run(run_autoassist(
    username=settings['username'],
    password=settings['password'],
    open_window_interval=settings.get('open_window_interval', None),
    geofencing_interval=settings.get('geofencing_interval', None),
))
