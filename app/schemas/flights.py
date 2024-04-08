from datetime import date, time

from pydantic import BaseModel


class Flight(BaseModel):
    flight_departure_date: date
    flight_departure_time: time
    flight_arrival_date: date
    flight_arrival_time: time
    departure_airport: str
    arrival_airport: str
