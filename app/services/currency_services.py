from datetime import datetime

from app.schemas.currency import Currency
from app.utils.constants import *


def parse_currency_information(response: dict, amount: float):
    conversion_rate = response["conversion_rate"]
    conversion = conversion_rate * amount
    return Currency(
        base_code=response["base_code"],
        target_code=response["target_code"],
        conversion=conversion,
    )
