import requests  # Добавлен импорт модуля requests
import unittest
from unittest.mock import patch, MagicMock
from src.external_api import convert_to_rubles, process_transaction



class TestExternalApi(unittest.TestCase):

    @patch('src.external_api.requests.get')
    def test_convert_usd_to_rub(self, mock_get):
        mock_response = MagicMock()
        # ИМИТИРУЕМ РЕАЛЬНЫЙ ОТВЕТ API: уже умноженная сумма!
        mock_response.json.return_value = {"success": True, "result": 7500.0}  # 100 × 75.0
        mock_response.status_code = 200
        mock_get.return_value = mock_response

        result = convert_to_rubles(100, "USD")
        print(f"DEBUG: result = {result}")  # Теперь будет 7500.0
        self.assertEqual(result, 7500.0)  # Тест пройдёт!

    @patch('src.external_api.os.getenv')
    def test_missing_api_key(self, mock_env):
        # Имитация отсутствия API-ключа
        mock_env.return_value = None
        with self.assertRaises(ValueError):
            convert_to_rubles(100, "USD")

    @patch('src.external_api.requests.get')
    def test_failed_request(self, mock_get):
        # Ошибка при обращении к API
        mock_response = MagicMock()
        mock_response.status_code = 400
        mock_response.json.return_value = {"success": False, "error": {"info": "Invalid API key"}}
        mock_get.return_value = mock_response

        with self.assertRaises(Exception):
            convert_to_rubles(100, "USD")

    @patch('src.external_api.requests.get')
    def test_network_error(self, mock_get):
        # Мок-объект для симуляции сетевой ошибки
        mock_get.side_effect = requests.exceptions.RequestException("Network error")
        with self.assertRaises(Exception):
            convert_to_rubles(100, "USD")

    @patch('src.external_api.convert_to_rubles')
    def test_process_transaction_in_rub(self, mock_convert):
        # Когда валюта изначально в рублях, конвертация не должна происходить
        transaction = {"amount": 1000, "currency": "RUB"}
        result = process_transaction(transaction)
        self.assertEqual(result, 1000.0)
        mock_convert.assert_not_called()

    @patch('src.external_api.convert_to_rubles')
    def test_process_transaction_usd(self, mock_convert):
        # Операция с долларом вызывает конверсию
        mock_convert.return_value = 7500.0
        transaction = {"amount": 100, "currency": "USD"}
        result = process_transaction(transaction)
        self.assertEqual(result, 7500.0)
        mock_convert.assert_called_once_with(100, "USD")

    def test_invalid_currency(self):
        # Неправильная валюта вызывает ошибку
        transaction = {"amount": 100, "currency": "GBP"}
        with self.assertRaises(ValueError):
            process_transaction(transaction)

    def test_non_string_currency(self):
        # Неверный тип валюты тоже приведёт к исключению
        transaction = {"amount": 100, "currency": 123}
        with self.assertRaises(TypeError):
            process_transaction(transaction)
