import unittest
from unittest.mock import patch, Mock
from datetime import datetime

from src.widget import mask_account_card, get_date



class TestMaskAccountCard(unittest.TestCase):

    @patch('src.widget.get_mask_card_number')  # ← Исправлен путь!
    def test_mask_card_visa(self, mock_get_mask_card):
        mock_get_mask_card.return_value = "1234 56** **** 7890"


        result = mask_account_card("visa 1234567890123456")
        self.assertEqual(result, "1234 56** **** 7890")  # ← Исправлено ожидаемое значение
        mock_get_mask_card.assert_called_once_with("1234567890123456")

    @patch('src.widget.get_mask_card_number')  # ← Исправлен путь!
    def test_mask_card_mastercard(self, mock_get_mask_card):
        mock_get_mask_card.return_value = "4444 44** **** 4444"
        result = mask_account_card("mastercard 4444444444444444")
        self.assertEqual(result, "4444 44** **** 4444")
        mock_get_mask_card.assert_called_once_with("4444444444444444")

    @patch('src.widget.get_mask_account')  # ← Исправлен путь!
    def test_mask_account(self, mock_get_mask_account):
        mock_get_mask_account.return_value = "**7890"
        result = mask_account_card("счет 1234567890")
        self.assertEqual(result, "**7890")
        mock_get_mask_account.assert_called_once_with("1234567890")


    def test_no_digits(self):
        result = mask_account_card("Нет цифр тут")
        self.assertEqual(result, "None")


    def test_non_digit_in_number(self):
        result = mask_account_card("Visa 123a567890123456")
        self.assertEqual(result, "None")


    def test_unknown_type(self):
        result = mask_account_card("Дебет 1234567890123456")
        self.assertEqual(result, "None")


class TestGetDate(unittest.TestCase):

    @patch('src.widget.datetime')  # ← Ключевое изменение!
    def test_get_date_valid(self, mock_datetime):
        # Мокируем fromisoformat внутри локального datetime
        mock_datetime.fromisoformat = Mock(
            return_value=datetime(2024, 3, 11, 2, 26, 18, 671407)
        )

        result = get_date("2024-03-11T02:26:18.671407")
        self.assertEqual(result, "11.03.2024")

        # Проверяем, что fromisoformat был вызван с правильным аргументом
        mock_datetime.fromisoformat.assert_called_once_with(
            "2024-03-11T02:26:18.671407"
        )

    def test_get_date_invalid_format(self):
        with self.assertRaises(ValueError):
            get_date("не-дата")

if __name__ == '__main__':
    unittest.main()
