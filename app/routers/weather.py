from fastapi import APIRouter, Depends

from app.ext.tomorrow import *
from app.schemas.weather import FiveDayWeather
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
def location_weather(location: str):
    try:
        return get_weather_info(location)
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)
