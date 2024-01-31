import os
from datetime import date

from fastapi import APIRouter

from app.ext.amadeus import *
from app.schemas.flights import Flight
from app.services.flight_services import *
from app.utils.api_exception import APIException, APIExceptionToHTTP
from app.utils.constants import *

router = APIRouter()


@router.get(
    "/flights",
    tags=["External services"],
    status_code=200,
    description="Flights status",
    response_model=Flight,
)
def flight_information(carrier_code: str, flight_number: str, departure_date: date):
    try:
        return get_flight_info(carrier_code, flight_number, departure_date)
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)
