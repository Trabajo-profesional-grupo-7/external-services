from datetime import date
from typing import List

from pydantic import BaseModel


class Weather(BaseModel):
    humidity: int
    cloudCover: int
    precipitation_probability: int
    temperature: float
    uv_index: int
    visibility: float


class DayWeather(BaseModel):
    date: date
    weather: Weather


class FiveDayWeather(BaseModel):
    location: str
    five_day_weather: List[DayWeather]
