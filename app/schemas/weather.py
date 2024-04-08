from datetime import date, time

from pydantic import BaseModel


class Weather(BaseModel):
    humidity: int
    precipitation_probability: int
    temperature: float
    uv_index: int
    visibility: float
