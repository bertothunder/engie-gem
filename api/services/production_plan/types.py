from typing import Dict, List
from pydantic import BaseModel, validator


class PowerPlant(BaseModel):
    name: str
    type: str
    efficiency: float
    pmin: int
    pmax: int

    @validator('efficiency')
    def check_efficiency_value(cls, v):
        if int(v) >= 1:
            raise ValueError('Plan efficiency can not be bigger than 1')
        return v

    @validator('pmin')
    def check_pmin_not_below_zero(cls, v):
        if v < 0:
            raise ValueError('Minimum value for plant pmin is 0')
        return v

    @validator('pmin', 'pmax')
    def check_min_below_pmax(cls, v, values, **kwargs):
        print(v, values, **kwargs)
        return v


class PowerPlantPayload(BaseModel):
    load: int
    fuels: Dict
    powerplants: List[PowerPlant]

    @validator('fuels')
    def check_necessary_fuels_info_provided(cls, v):
        print(v)
        if ('gas(euro/MWh)', 'kerosine(euro/MWh)', 'wind(%)') not in v:
            raise ValueError('The "fuels" field does not contain all energy costs and wind efficiency fields')
        return v
