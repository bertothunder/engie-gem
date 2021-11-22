import os
import json
import sys
from functools import lru_cache
from pydantic import BaseSettings


PROJECT_NAME: str = "Engine Gem SPAAS"

LISTEN_HOST: str = os.getenv("HOST", "127.0.0.1")
LISTEN_PORT: int = int(os.getenv("PORT", 8888))
BASE_URL: str = f"http://{LISTEN_HOST}:{LISTEN_PORT}"

# Debug and Logging format
DEBUG: bool = True if os.getenv("DEBUG", "False").upper() in ("TRUE", "1") else False
LOG_FORMAT: str = "%(asctime)s - %(levelname)s - %(name)s:%(filename)s:%(lineno)d - %(message)s"
LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")


# Load in an environment specific config file the build process maps environment variables
env_config_file = os.getenv("CFG_FILE", "config/dev.json")
if env_config_file and os.path.exists(env_config_file):
    with open(env_config_file, "r") as stream:
        config = json.load(stream)
    for item in config.keys():
        setattr(sys.modules[__name__], item.upper(), config[item])


class AppSettings(BaseSettings):
    project_name: str = PROJECT_NAME

    listen_host: str = LISTEN_HOST
    listen_port: int = LISTEN_PORT
    base_url: str = BASE_URL

    # Debug and Logging format
    debug: bool = DEBUG
    log_format: str = LOG_FORMAT
    log_level: str = LOG_LEVEL

    services = [
        "api.services.production_plan",
    ]


@lru_cache(maxsize=128)
def get_app_settings() -> AppSettings:
    return AppSettings()  # reads variables from environment
