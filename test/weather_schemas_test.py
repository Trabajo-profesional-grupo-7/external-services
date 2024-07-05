import unittest
from datetime import date
from typing import List
from unittest.mock import Mock

from pydantic import ValidationError

from app.schemas.weather import DayWeather, FiveDayWeather, Weather


class TestWeatherSchemas(unittest.TestCase):

    def test_weather_model_valid(self):
        data = {
            "humidity": 70,
            "cloudCover": 50,
            "precipitation_probability": 20,
            "temperature": 25.5,
            "uv_index": 5,
            "visibility": 10.0,
        }
        weather = Weather(**data)
        self.assertEqual(weather.humidity, 70)
        self.assertEqual(weather.cloudCover, 50)
        self.assertEqual(weather.precipitation_probability, 20)
        self.assertEqual(weather.temperature, 25.5)
        self.assertEqual(weather.uv_index, 5)
        self.assertEqual(weather.visibility, 10.0)

    def test_day_weather_model(self):
        date_obj = date(2024, 7, 10)
        weather_data = {
            "humidity": 70,
            "cloudCover": 50,
            "precipitation_probability": 20,
            "temperature": 25.5,
            "uv_index": 5,
            "visibility": 10.0,
        }
        day_weather_data = {"date": date_obj, "weather": Weather(**weather_data)}
        day_weather = DayWeather(**day_weather_data)
        self.assertEqual(day_weather.date, date_obj)
        self.assertEqual(day_weather.weather.humidity, 70)
        self.assertEqual(day_weather.weather.temperature, 25.5)

    def test_five_day_weather_model(self):
        date_obj = date(2024, 7, 10)
        weather_data = {
            "humidity": 70,
            "cloudCover": 50,
            "precipitation_probability": 20,
            "temperature": 25.5,
            "uv_index": 5,
            "visibility": 10.0,
        }
        day_weather_data = {"date": date_obj, "weather": Weather(**weather_data)}
        five_day_weather_data = {
            "location": "CABA",
            "five_day_weather": [DayWeather(**day_weather_data)],
        }
        five_day_weather = FiveDayWeather(**five_day_weather_data)
        self.assertEqual(five_day_weather.location, "CABA")
        self.assertEqual(len(five_day_weather.five_day_weather), 1)
        self.assertEqual(five_day_weather.five_day_weather[0].date, date_obj)
