import os

import requests
from fastapi import status

from app.services.currency_services import parse_currency_information
from app.utils.api_exception import APIException, APIExceptionToHTTP
from app.utils.constants import *

API_KEY = os.getenv("EXCHANGERATE_API_KEY")

api_url = "https://v6.exchangerate-api.com/v6"


def get_currency_info(currency: str, interest_currency: str, amount: float):
    try:
        url = f"{api_url}/{API_KEY}/pair/{currency}/{interest_currency}"

        headers = {"accept": "application/json"}
        response = requests.get(url=url, headers=headers)

        if response.status_code != 200:
            raise APIException(code=EXTERNAL_SERVICE_ERROR, msg="")
        response_data = response.json()

        return parse_currency_information(response_data, amount)
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)
