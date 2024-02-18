from fastapi import APIRouter, Depends

from app.ext.exchange_rate import get_currency_info
from app.schemas.currency import Currency
from app.utils.api_exception import APIException, APIExceptionToHTTP
from app.utils.constants import *

router = APIRouter()


@router.get(
    "/currency",
    tags=["Currency"],
    status_code=200,
    description="Currency conversion",
    response_model=Currency,
)
def currency_conversor(currency: str, interest_currency: str, amount: float):
    try:
        return get_currency_info(currency, interest_currency, amount)
    except APIException as e:
        raise APIExceptionToHTTP().convert(e)
