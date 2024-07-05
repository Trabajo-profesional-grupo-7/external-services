import unittest
from unittest.mock import Mock

from pydantic import ValidationError

from app.schemas.currency import Currency


class TestCurrencySchema(unittest.TestCase):

    def test_currency_model_valid(self):
        data = {"base_code": "USD", "target_code": "EUR", "conversion": 0.85}
        currency = Currency(**data)
        self.assertEqual(currency.base_code, "USD")
        self.assertEqual(currency.target_code, "EUR")
        self.assertEqual(currency.conversion, 0.85)

    def test_currency_model_invalid(self):
        data = {"base_code": "USD", "target_code": "EUR", "conversion": "invalid"}
        with self.assertRaises(ValidationError):
            Currency(**data)
