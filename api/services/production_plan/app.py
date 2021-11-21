import logging
from api.core.exceptions import NotFoundException
from api.settings import get_app_settings, AppSettings
from fastapi import APIRouter, Response, Depends
from api.services.production_plan.types import PowerPlantPayload


api = APIRouter()
logger = logging.getLogger("api.services.production_plan")


@api.post(path="/productionplan")
async def calculate_production_plan(
    power_plant_payload: PowerPlantPayload,
    settings: AppSettings = Depends(get_app_settings),
) -> Response:

    raise NotFoundException()


