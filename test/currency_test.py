from unittest.mock import patch

import pytest

from app.schemas.currency import Currency
from app.services.currency_services import parse_currency_information


def test_parse_currency_information():

    mock_response = {
        "result": "success",
        "time_last_update_unix": 1719187201,
        "time_last_update_utc": "Mon, 24 Jun 2024 00:00:01 +0000",
        "time_next_update_unix": 1719273601,
        "time_next_update_utc": "Tue, 25 Jun 2024 00:00:01 +0000",
        "base_code": "USD",
        "target_code": "EUR",
        "conversion_rate": 0.9354,
    }

    with patch(
        "app.services.currency_services.parse_currency_information",
        return_value=Currency(base_code="USD", target_code="EUR", conversion=93.54),
    ):

        result = parse_currency_information(mock_response, 100)

    assert result.base_code == "USD"
    assert result.target_code == "EUR"
    assert result.conversion == 93.54
