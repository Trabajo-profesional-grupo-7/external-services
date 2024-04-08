from datetime import datetime

from app.schemas.weather import Weather
from app.utils.constants import *


def parse_weather_info(response: dict):
    weather_data = response["data"]["values"]

    return Weather(
        humidity=weather_data["humidity"],
        precipitation_probability=weather_data["precipitationProbability"],
        temperature=weather_data["temperature"],
        uv_index=weather_data["uvIndex"],
        visibility=weather_data["visibility"],
    )
