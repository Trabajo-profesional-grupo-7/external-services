import os

import requests
from fastapi import status

from app.services.weather_services import parse_five_day_weather_info
from app.utils.api_exception import APIException, APIExceptionToHTTP
from app.utils.constants import *

API_KEY = os.getenv("TOMORROW_API_KEY")

api_url = "https://api.tomorrow.io/v4/weather/forecast"


def get_weather_info(location: str):
    try:
        headers = {"accept": "application/json"}
        timestamp = "1d"
        params = {"location": location, "timesteps": timestamp, "apikey": API_KEY}
        response = requests.get(url=api_url, params=params)

        if response.status_code != 200:
            raise APIException(code=EXTERNAL_SERVICE_ERROR, msg="")
        response_data = response.json()

        return parse_five_day_weather_info(response_data, location)
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)
