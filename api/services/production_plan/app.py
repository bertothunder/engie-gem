import json
import anyio
import typing
import logging
from fastapi import APIRouter
from api.services.production_plan.types import PowerPlantPayload, PerPlanCalculationsPayload
from api.services.production_plan.controller import process


api = APIRouter()
logger = logging.getLogger("api.services.production_plan")


@api.post(path="/productionplan", response_model=typing.List[PerPlanCalculationsPayload])
async def calculate_production_plan(payload: PowerPlantPayload):
    data = json.loads(payload.json())
    # In FastAPI is not possible to run sync code in a different thread, unless using AnyIO primitives to run
    # sync in a worker thread, which allows it to keep being async and improved performance
    return await anyio.to_thread.run_sync(process, data)
