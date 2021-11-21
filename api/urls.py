import logging
from importlib import import_module
from fastapi import APIRouter

from api.settings import get_app_settings


router = APIRouter()
logger = logging.getLogger('api.main.settings')
settings = get_app_settings()


logger.info(settings.services)
for s in settings.services:
    module = import_module(f"{s}.urls")
    router.include_router(module.router)
