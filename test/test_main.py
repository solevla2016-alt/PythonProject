import unittest
import json
import os
from tempfile import NamedTemporaryFile
from unittest.mock import patch, Mock
from src.main import *
from datetime import datetime
from io import StringIO
from contextlib import redirect_stdout
import sys


class TestMainFunctions(unittest.TestCase):

    def setUp(self):
        self.maxDiff = None

    @patch('sys.stdout', new_callable=StringIO)
    def test_get_mask_card_number_valid(self, mock_stdout):
        result = get_mask_card_number("1234567890123456")
        expected_result = "1234 56** **** 3456"
        self.assertEqual(result, expected_result)

    @patch('sys.stdout', new_callable=StringIO)
    def test_get_mask_card_number_invalid_length(self, mock_stdout):
        result = get_mask_card_number("123456789012345")
        expected_result = ""
        self.assertEqual(result, expected_result)

    @patch('sys.stdout', new_callable=StringIO)
    def test_get_mask_account_valid(self, mock_stdout):
        result = get_mask_account("1234567890123456")
        expected_result = "**3456"
        self.assertEqual(result, expected_result)


    @patch('sys.stdout', new_callable=StringIO)
    def test_mask_account_card_visa(self, mock_stdout):
        result = mask_account_card("Visa 1234567890123456")
        expected_result = "1234 56** **** 3456"
        self.assertEqual(result, expected_result)

    @patch('sys.stdout', new_callable=StringIO)
    def test_mask_account_card_mastercard(self, mock_stdout):
        result = mask_account_card("MasterCard 1234567890123456")
        expected_result = "1234 56** **** 3456"
        self.assertEqual(result, expected_result)

    @patch('sys.stdout', new_callable=StringIO)
    def test_mask_account_card_account(self, mock_stdout):
        result = mask_account_card("Счет 1234567890123456")
        expected_result = "**3456"
        self.assertEqual(result, expected_result)

    @patch('sys.stdout', new_callable=StringIO)
    def test_get_date_iso_format(self, mock_stdout):
        iso_date = "2023-10-05T14:30:00Z"
        result = get_date(iso_date)
        expected_result = "05.10.2023"
        self.assertEqual(result, expected_result)

    def setUp(self):
        self.maxDiff = None

    @patch('builtins.input')
    @patch('src.utils.load_transactions')
    @patch('src.processing.filter_by_state')
    @patch('src.processing.sort_by_date')
    @patch('src.external_api.process_transaction')
    def test_main_functionality_json_with_temporary_file(
        self,
        mock_process_transaction,
        mock_sort_by_date,
        mock_filter_by_state,
        mock_load_transactions,
        mock_input
    ):
        # Создание временной копии файла
        temp_file = NamedTemporaryFile(mode="w+", delete=False)
        transaction_data = [{
            "id": 1,
            "date": "2023-10-05T14:30:00Z",
            "description": "Перевод средств",
            "from": "Visa 1234567890123456",
            "to": "Счет 1234567890123456",
            "operationAmount": {
                "amount": "1000",
                "currency": {
                    "code": "RUB",
                    "name": "Российский рубль"
                }
            },
            "state": "EXECUTED"
        }]
        json.dump(transaction_data, temp_file)
        temp_file.close()

        mock_input.side_effect = ["1", temp_file.name, "EXECUTED", "Да", "По убыванию", "Да", "нет"]
        mock_load_transactions.return_value = transaction_data
        mock_filter_by_state.return_value = mock_load_transactions.return_value
        mock_sort_by_date.return_value = mock_load_transactions.return_value
        mock_process_transaction.return_value = float(mock_load_transactions.return_value[0]["operationAmount"]["amount"])

        with patch('sys.stdout', new=StringIO()) as fake_out:
            main()
            output = fake_out.getvalue()

        # Ключевые элементы для проверки
        key_elements = [
            "Программа: Привет!",
            "Получить информацию о транзакциях из JSON-файла",
            "Операции отфильтрованы по статусу \"EXECUTED\"",
            "Распечатываю итоговый список транзакций...",
            "Всего банковских операций в выборке: 1",
            "05.10.2023 Перевод средств",
            "1234 56** **** 3456 -> **3456",
            "Сумма: 1000.0 Российский рубль",
            "Работа завершена.",
        ]

        # Проверяем наличие ключевых элементов в выводе
        for element in key_elements:
            self.assertIn(element, output)

        # Удаляем временный файл
        os.unlink(temp_file.name)


class TestMainErrorsHandling(unittest.TestCase):

    @patch('sys.stdout', new_callable=StringIO)
    def test_invalid_file_path_no_exit(self, mock_stdout):
        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ['1', '/nonexistent/path/to/file.json']

            main()  # Просто выполняем main(), проверяя вывод без SystemExit

        self.assertIn("Файл не найден:", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_empty_file(self, mock_stdout):
        temp_file = NamedTemporaryFile(delete=False)
        temp_file.write(b"[]")
        temp_file.close()

        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ['1', temp_file.name]

            main()

        self.assertIn("Ошибка загрузки данных или файл пуст", mock_stdout.getvalue())

    @patch('sys.stdout', new_callable=StringIO)
    def test_missing_fields_in_data(self, mock_stdout):
        temp_file = NamedTemporaryFile(delete=False)
        invalid_data = [{
            "id": 1,
            "description": "Тестовая операция",
            "state": "EXECUTED"
        }]
        json.dump(invalid_data, open(temp_file.name, 'w'))

        with patch('builtins.input') as mock_input:
            mock_input.side_effect = ['1', temp_file.name, 'EXECUTED']

            main()

        # Проверяем наличие стандартной ошибки
        self.assertIn("Произошла ошибка:", mock_stdout.getvalue())

class TestMaskAccountCard(unittest.TestCase):
    def test_mask_short_card_number(self):
        result = mask_account_card("Visa 123456789012345")
        expected_result = "None"
        self.assertEqual(result, expected_result)

    def test_mask_long_card_number(self):
        result = mask_account_card("Visa 12345678901234567890")
        expected_result = "None"
        self.assertEqual(result, expected_result)

    def test_mask_account_short_number(self):
        result = mask_account_card("Счет 1234567890123456")
        expected_result = "**3456"
        self.assertEqual(result, expected_result)

    def test_mask_account_too_short_number(self):
        result = mask_account_card("Счет 1234")
        expected_result = "**1234"
        self.assertEqual(result, expected_result)

    def test_mask_account_minimal_number(self):
        result = mask_account_card("Счет 12345678")
        expected_result = "**5678"
        self.assertEqual(result, expected_result)


if __name__ == '__main__':
    unittest.main()