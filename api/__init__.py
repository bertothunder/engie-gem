from fastapi import FastAPI
import logging
import logging.config

from api.core.exceptions import APIException, api_exception_handler
from .urls import router
from .settings import get_app_settings, AppSettings


def setup_logging(app_settings: AppSettings):
    """
    Configure the logger
    :return:
    """
    level = logging.getLevelName(app_settings.log_level)
    # Override logging level to debug if debug settings are enabled
    if app_settings.debug:
        level = logging.DEBUG

    log_config = {
        "version": 1,
        "disable_existing_loggers": 0,
        "root": {
            "level": level,
            "handlers": [
                "console",
            ],
        },
        "loggers": {},
        "formatters": {"default": {"format": app_settings.log_format}},
        "handlers": {
            "console": {
                "formatter": "default",
                "class": "logging.StreamHandler",
                "level": level,
            }
        },
    }
    logging.config.dictConfig(log_config)


def create_app(testing: bool = False) -> FastAPI:
    """
    Prepares the app instance, connects to database and
    sets up all the different parts.
    :param testing:
    :return:
    """
    app_settings = get_app_settings()
    setup_logging(app_settings)
    app = FastAPI(title="Engie API", openapi_url="/openapi")

    app.state.testing = testing

    @app.on_event("shutdown")
    def shutdown() -> None:
        logging.getLogger("main").info("API shutdown...")

    app.add_exception_handler(APIException, api_exception_handler)
    app.include_router(router)
    return app
