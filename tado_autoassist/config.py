
from dynaconf import Dynaconf

settings = Dynaconf(
    envvar_prefix="TADO_AA",
    settings_files=['settings.toml', '.secrets.toml'],
)
