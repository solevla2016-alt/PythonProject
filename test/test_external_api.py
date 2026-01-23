import unittest
from unittest.mock import patch, MagicMock
from src.external_api import (
    _get_exchange_rate,
    convert_to_rubles,
    process_transaction
)


class TestCurrencyConversion(unittest.TestCase):

    @patch('requests.get')
    def test_get_exchange_rate_success(self, mock_requests_get):
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'result': 65.5}

        mock_requests_get.return_value = mock_response

        result = _get_exchange_rate('USD', 'RUB')
        self.assertEqual(result, 65.5)

    @patch('src.external_api._get_exchange_rate')  # было: 'main._get_exchange_rate'
    def test_convert_to_rubles(self, mock_getexchange_rate):
        mock_getexchange_rate.return_value = 65.5
        result = convert_to_rubles(100, 'USD')
        self.assertAlmostEqual(result, 6550.0, places=2)

    def test_process_transaction_valid_input(self):
        valid_transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {
                    "code": "USD"
                }
            }
        }
        with patch('src.external_api.convert_to_rubles') as mock_convert:  # было: 'main.convert_to_rubles'
            mock_convert.return_value = 6550.0
            result = process_transaction(valid_transaction)
            self.assertEqual(result, 6550.0)

    def test_process_transaction_missing_operation_amount(self):
        invalid_transaction = {}
        with self.assertRaises(KeyError):
            process_transaction(invalid_transaction)

    def test_process_transaction_invalid_amount_type(self):
        invalid_transaction = {
            "operationAmount": {
                "amount": {},
                "currency": {
                    "code": "USD"
                }
            }
        }
        with self.assertRaises(TypeError):
            process_transaction(invalid_transaction)

    def test_process_transaction_negative_amount(self):
        invalid_transaction = {
            "operationAmount": {
                "amount": "-100",
                "currency": {
                    "code": "USD"
                }
            }
        }
        with self.assertRaises(ValueError):
            process_transaction(invalid_transaction)

    def test_process_transaction_unsupported_currency(self):
        invalid_transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {
                    "code": "GBP"
                }
            }
        }
        with self.assertRaises(ValueError):
            process_transaction(invalid_transaction)


if __name__ == '__main__':
    unittest.main()