import os

import requests
from fastapi import status

from app.services.currency_services import parse_currency_information
from app.services.location_iq import get_user_city
from app.utils.api_exception import APIException, APIExceptionToHTTP
from app.utils.constants import *

LOCATION_IQ_API_KEY = os.getenv("LOCATION_IQ_API_KEY")

API_URL = "https://us1.locationiq.com/v1/reverse.php"


def get_gelocation(latitude: float, longitude: float):
    try:

        params = {
            "key": LOCATION_IQ_API_KEY,
            "lat": latitude,
            "lon": longitude,
            "format": "json",
        }

        response = requests.get(API_URL, params=params)

        if response.status_code != 200:
            raise APIException(code=EXTERNAL_SERVICE_ERROR, msg="")
        return get_user_city(response.json())

    except APIException as e:
        raise APIExceptionToHTTP().convert(e)
