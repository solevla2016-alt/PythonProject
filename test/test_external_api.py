import unittest
from unittest.mock import patch, MagicMock
import requests  # Нужен для моков исключений
from src.external_api import (
    _get_exchange_rate,
    convert_to_rubles,
    process_transaction
)



class TestCurrencyConversion(unittest.TestCase):

    # --- Тесты для _get_exchange_rate ---


    @patch('requests.get')
    def test_get_exchange_rate_success(self, mock_requests_get):
        """Успешный ответ API с курсом."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'result': 65.5}
        mock_requests_get.return_value = mock_response

        result = _get_exchange_rate('USD', 'RUB')
        self.assertEqual(result, 65.5)

    @patch('requests.get')
    def test_get_exchange_rate_api_error_response(self, mock_requests_get):
        """Ответ API с полем 'error'."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = {'error': {'info': 'Invalid API key'}}
        mock_requests_get.return_value = mock_response


        with self.assertRaises(Exception) as cm:
            _get_exchange_rate('USD', 'RUB')
        self.assertIn('API ошибка: Invalid API key', str(cm.exception))


    @patch('requests.get')
    def test_get_exchange_rate_invalid_json(self, mock_requests_get):
        """Невалидный JSON от API (не словарь)."""
        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.return_value = "not a dict"
        mock_requests_get.return_value = mock_response


        with self.assertRaises(Exception) as cm:
            _get_exchange_rate('USD', 'RUB')
        self.assertIn('Неверный формат ответа API', str(cm.exception))


    @patch('requests.get')
    def test_get_exchange_rate_request_timeout_first_attempt(self, mock_requests_get):
        """Таймаут на первой попытке, успех на второй."""
        mock_requests_get.side_effect = [
            requests.exceptions.Timeout('Timeout on first try'),
            MagicMock(status_code=200, json=lambda: {'result': 65.5})
        ]

        result = _get_exchange_rate('USD', 'RUB')
        self.assertEqual(result, 65.5)
        self.assertEqual(mock_requests_get.call_count, 2)


    @patch('requests.get')
    def test_get_exchange_rate_request_fails_both_attempts(self, mock_requests_get):
        """Обе попытки запроса провалились."""
        mock_requests_get.side_effect = [
            requests.exceptions.ConnectionError('First fail'),
            requests.exceptions.Timeout('Second fail')
        ]

        with self.assertRaises(Exception) as cm:
            _get_exchange_rate('USD', 'RUB')
        self.assertIn('Ошибка запроса к API после 2 попыток', str(cm.exception))


    @patch('requests.get')
    def test_get_exchange_rate_http_error(self, mock_requests_get):
        """HTTP-ошибка (например, 400)."""
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.raise_for_status.side_effect = requests.exceptions.HTTPError('Bad Request')
        mock_requests_get.return_value = mock_response


        with self.assertRaises(Exception):
            _get_exchange_rate('USD', 'RUB')


    # --- Тесты для convert_to_rubles ---


    @patch('src.external_api._get_exchange_rate')
    def test_convert_to_rubles_success(self, mock_getexchange_rate):
        """Успешная конвертация суммы."""
        mock_getexchange_rate.return_value = 65.5
        result = convert_to_rubles(100, 'USD')
        self.assertAlmostEqual(result, 6550.0, places=2)


    @patch('src.external_api._get_exchange_rate')
    def test_convert_to_rubles_network_error(self, mock_getexchange_rate):
        """Сетевая ошибка при запросе курса."""
        mock_getexchange_rate.side_effect = requests.exceptions.RequestException('Network issue')


        with self.assertRaises(RuntimeError) as cm:
            convert_to_rubles(100, 'USD')
        self.assertIn('Сетевой сбой при запросе курса USD→RUB', str(cm.exception))


    @patch('src.external_api._get_exchange_rate')
    def test_convert_to_rubles_general_exception(self, mock_getexchange_rate):
        """Общая ошибка при получении курса."""
        mock_getexchange_rate.side_effect = Exception('Unknown error')


        with self.assertRaises(RuntimeError) as cm:
            convert_to_rubles(100, 'USD')
        self.assertIn('Ошибка получения курса USD→RUB', str(cm.exception))


    # --- Тесты для process_transaction ---

    def test_process_transaction_valid_input_rub(self):
        """Транзакция в RUB (конвертация вызывается с теми же значениями)."""
        valid_transaction = {
            "operationAmount": {
                "amount": "5000",
                "currency": {
                    "code": "RUB"
                }
            }
        }
        with patch('src.external_api.convert_to_rubles') as mock_convert:
            mock_convert.return_value = 5000.0
            result = process_transaction(valid_transaction)
            self.assertEqual(result, 5000.0)
            mock_convert.assert_called_once_with(5000.0, 'RUB')


    def test_process_transaction_missing_operationamount(self):
        """Отсутствует поле operationAmount."""
        invalid_transaction = {}
        with self.assertRaises(KeyError) as cm:
            process_transaction(invalid_transaction)
        self.assertIn("Поле 'operationAmount' отсутствует", str(cm.exception))


    def test_process_transaction_missing_amount(self):
        """Отсутствует поле amount."""
        invalid_transaction = {"operationAmount": {"currency": {"code": "USD"}}}
        with self.assertRaises(KeyError) as cm:
            process_transaction(invalid_transaction)
        self.assertIn("Поле 'operationAmount.amount' отсутствует", str(cm.exception))


    def test_process_transaction_missing_currency_code(self):
        """Отсутствует поле currency.code."""
        invalid_transaction = {
            "operationAmount": {
                "amount": "100",
                "currency": {}
            }
        }
        with self.assertRaises(KeyError) as cm:
            process_transaction(invalid_transaction)
        self.assertIn("Поле 'operationAmount.currency.code' отсутствует", str(cm.exception))


    def test_process_transaction_invalid_amount_type(self):
        """Поле amount не число/строка."""
        invalid_transaction = {
            "operationAmount": {
                "amount": {},
                "currency": {"code": "USD"}
            }
        }
        with self.assertRaises(TypeError) as cm:
            process_transaction(invalid_transaction)
        self.assertIn("должно быть числом или строкой", str(cm.exception))


    def test_process_transaction_empty_amount_string(self):
        """Пустая строка в amount."""
        invalid_transaction = {
            "operationAmount": {
                "amount": "",
                "currency": {"code": "USD"}
            }
        }
        with self.assertRaises(ValueError) as cm:
            process_transaction(invalid_transaction)
        self.assertIn("не может быть пустой строкой", str(cm.exception))
