from datetime import date, datetime

from app.schemas.weather import DayWeather, FiveDayWeather, Weather
from app.utils.constants import *


def get_location(city: str, province: str, country: str):
    return " ".join(filter(None, [city, province, country]))


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
            humidity=int(values.get("humidityAvg")),
            cloudCover=int(values.get("cloudCoverAvg", 0)),
            precipitation_probability=int(values.get("precipitationProbabilityAvg")),
            temperature=values.get("temperatureAvg"),
            uv_index=int(values.get("uvIndexAvg", 0)),
            visibility=values.get("visibilityAvg"),
        )
        day_weather = DayWeather(date=date_time, weather=weather)
        five_day_weather_info.append(day_weather)

    return FiveDayWeather(location=location, five_day_weather=five_day_weather_info)
