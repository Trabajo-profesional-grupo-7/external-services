import unittest
from datetime import date, time
from unittest.mock import Mock

from pydantic import ValidationError

from app.schemas.flights import Flight


class TestFlightSchema(unittest.TestCase):

    def test_flight_model_valid(self):
        data = {
            "flight_departure_date": date(2024, 7, 10),
            "flight_departure_time": time(8, 30),
            "flight_arrival_date": date(2024, 7, 10),
            "flight_arrival_time": time(11, 0),
            "departure_airport": "EZE",
            "arrival_airport": "MIA",
        }
        flight = Flight(**data)
        self.assertEqual(flight.flight_departure_date, date(2024, 7, 10))
        self.assertEqual(flight.flight_departure_time, time(8, 30))
        self.assertEqual(flight.flight_arrival_date, date(2024, 7, 10))
        self.assertEqual(flight.flight_arrival_time, time(11, 0))
        self.assertEqual(flight.departure_airport, "EZE")
        self.assertEqual(flight.arrival_airport, "MIA")
