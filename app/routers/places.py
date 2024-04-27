from typing import Optional

from fastapi import APIRouter

from app.ext.amadeus import *
from app.utils.api_exception import APIException, APIExceptionToHTTP
from app.utils.constants import *

router = APIRouter()


@router.get(
    "/Cities",
    tags=["Cities"],
    status_code=200,
    description="Get city name",
)
def flight_information(keyword: str):
    try:
        return get_places(keyword)
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)
