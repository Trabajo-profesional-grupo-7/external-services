from typing import Optional

from fastapi import APIRouter, Depends

from app.ext.tomorrow import *
from app.schemas.weather import FiveDayWeather
from app.services.weather_services import get_location
from app.utils.api_exception import APIException, APIExceptionToHTTP
from app.utils.constants import *

router = APIRouter()


@router.get(
    "/weather",
    tags=["Weather"],
    status_code=200,
    description="Location weather",
    response_model=FiveDayWeather,
)
def location_weather(
    city: str, province: Optional[str] = None, country: Optional[str] = None
):
    try:
        location = get_location(city, province, country)
        print(location)
        return get_weather_info(location)
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)
