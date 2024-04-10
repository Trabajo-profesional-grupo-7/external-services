from datetime import date, datetime

from app.schemas.weather import DayWeather, FiveDayWeather, Weather
from app.utils.constants import *


def parse_five_day_weather_info(response: dict, location: str):
    weather_data_list = response.get("timelines", {}).get("daily", [])
    five_day_weather_info = []

    for weather_data in weather_data_list:
        time = weather_data.get("time")
        if not time:
            continue
        values = weather_data.get("values", {})
        if not values:
            continue
        date_time = date.fromisoformat(time[:10])
        weather = Weather(
            humidity=int(values.get("humidityAvg", 0)),
            cloudCover=int(values.get("cloudCover", 0)),
            precipitation_probability=int(values.get("precipitationProbabilityAvg", 0)),
            temperature=values.get("temperatureAvg", 0),
            uv_index=values.get("uvIndexAvg", 0),
            visibility=values.get("visibilityAvg", 0),
        )
        day_weather = DayWeather(date=date_time, weather=weather)
        five_day_weather_info.append(day_weather)

    return FiveDayWeather(location=location, five_day_weather=five_day_weather_info)
