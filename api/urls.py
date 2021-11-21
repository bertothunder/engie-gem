from importlib import import_module
from fastapi import APIRouter

from api.settings import get_app_settings


router = APIRouter()


for s in get_app_settings().services:
    module = import_module(f"{s}.urls")
    router.include_router(module.router)
