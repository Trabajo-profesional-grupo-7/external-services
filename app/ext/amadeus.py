import os

from amadeus import Client, ResponseError
from fastapi import status

from app.services.flight_services import parse_flight_info
from app.utils.api_exception import APIException
from app.utils.constants import *

API_KEY = os.getenv("AMADEUS_API_KEY")
API_SECRET = os.getenv("AMADEUS_API_SECRET")

amadeus = Client(client_id=API_KEY, client_secret=API_SECRET)


def get_flight_info(carrier_code: str, flight_number: str, departure_date: str):
    try:
        response = amadeus.schedule.flights.get(
            carrierCode=carrier_code,
            flightNumber=flight_number,
            scheduledDepartureDate=departure_date,
        )

        if not response.data:
            raise APIException(
                code=FLIGTH_INFO_NOT_FOUND_ERROR, msg="FLIGHT INFORMATION NOT FOUND"
            )

        return parse_flight_info(response.data[0])
    except ResponseError as e:
        raise APIException(code=FLIGTH_INFO_NOT_FOUND_ERROR, msg=str(e))
