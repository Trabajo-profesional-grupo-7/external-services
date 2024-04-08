from datetime import datetime

from app.schemas.flights import Flight
from app.utils.constants import *


def parse_flight_info(response: dict):
    departure = response["flightPoints"][0]
    arrival = response["flightPoints"][1]

    departure_datetime = datetime.strptime(
        departure["departure"]["timings"][0]["value"], "%Y-%m-%dT%H:%M%z"
    )

    arrival_datetime = datetime.strptime(
        departure["departure"]["timings"][0]["value"], "%Y-%m-%dT%H:%M%z"
    )

    return Flight.model_construct(
        flight_departure_date=departure_datetime.date(),
        flight_departure_time=departure_datetime.time(),
        flight_arrival_date=arrival_datetime.date(),
        flight_arrival_time=arrival_datetime.time(),
        departure_airport=departure["iataCode"],
        arrival_airport=arrival["iataCode"],
    )
