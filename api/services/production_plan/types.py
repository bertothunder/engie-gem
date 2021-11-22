import logging
from typing import Dict, List
from pydantic import BaseModel, validator


logger = logging.getLogger("api.services.production_plan.types")


class PowerPlant(BaseModel):
    name: str
    type: str
    efficiency: float
    pmin: int
    pmax: int

    @validator("efficiency")
    def check_efficiency_value(cls, v):
        if v > 1.0:
            raise ValueError("Plant efficiency can not be bigger than 1")
        return v

    @validator("pmin")
    def check_pmin_not_below_zero(cls, v):
        if v < 0:
            raise ValueError("Minimum value for plant pmin is 0")
        return v


class PowerPlantPayload(BaseModel):
    load: int
    fuels: Dict
    powerplants: List[PowerPlant]


class PerPlanCalculationsPayload(BaseModel):
    name: str
    p: int


class CalculationsPayload(BaseModel):
    data: List[PerPlanCalculationsPayload]
