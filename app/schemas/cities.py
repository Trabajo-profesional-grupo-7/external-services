from typing import List

from pydantic import BaseModel


class City(BaseModel):
    name: str
    country: str
    state_code: str
    latitude: float
    longitude: float


class Cities(BaseModel):
    cities: List[City]
