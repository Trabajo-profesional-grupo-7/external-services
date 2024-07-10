import unittest
from typing import List
from unittest.mock import Mock

from pydantic import ValidationError

from app.schemas.cities import Cities, City


class TestCitySchema(unittest.TestCase):

    def test_city_model_valid(self):
        data = {
            "name": "CABA",
            "country": "Argentina",
            "state_code": "AR",
            "latitude": 40.7128,
            "longitude": -74.0060,
        }
        city = City(**data)
        self.assertEqual(city.name, "CABA")
        self.assertEqual(city.country, "Argentina")
        self.assertEqual(city.state_code, "AR")
        self.assertEqual(city.latitude, 40.7128)
        self.assertEqual(city.longitude, -74.0060)

    def test_city_model_invalid(self):
        data = {
            "name": "CABA",
            "country": "Argentina",
            "state_code": "AR",
            "latitude": "invalid",
            "longitude": -74.0060,
        }
        with self.assertRaises(ValidationError):
            City(**data)


class TestCitiesSchema(unittest.TestCase):

    def test_cities_model_valid(self):
        data = {
            "cities": [
                {
                    "name": "CABA",
                    "country": "Argentina",
                    "state_code": "AR",
                    "latitude": 40.7128,
                    "longitude": -74.0060,
                },
                {
                    "name": "Cordoba",
                    "country": "Argentina",
                    "state_code": "AR",
                    "latitude": 34.0522,
                    "longitude": -118.2437,
                },
            ]
        }
        cities = Cities(**data)
        self.assertIsInstance(cities.cities, list)
        self.assertEqual(len(cities.cities), 2)
        self.assertIsInstance(cities.cities[0], City)
        self.assertEqual(cities.cities[0].name, "CABA")
        self.assertEqual(cities.cities[1].name, "Cordoba")

    def test_cities_model_invalid(self):
        data = {
            "cities": [
                {
                    "name": "CABA",
                    "country": "Argentina",
                    "state_code": "AR",
                    "latitude": "invalid",
                    "longitude": -74.0060,
                },
                {
                    "name": "Cordoba",
                    "country": "Argentina",
                    "state_code": "AR",
                    "latitude": 34.0522,
                    "longitude": -118.2437,
                },
            ]
        }
        with self.assertRaises(ValidationError):
            Cities(**data)
