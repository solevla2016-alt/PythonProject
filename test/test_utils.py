import unittest
from unittest.mock import mock_open, patch
from src.utils import load_transactions
from unittest import TestCase


class TestLoadTransactions(unittest.TestCase):
    @patch("builtins.open", new_callable=mock_open, read_data="[]")
    def test_load_valid_json_list(self, mock_file):
        result = load_transactions('valid_file.json')
        self.assertEqual(result, [])

    @patch("builtins.open", side_effect=FileNotFoundError())
    def test_file_not_found(self, mock_file):
        result = load_transactions('missing_file.json')
        self.assertEqual(result, [])

    @patch("builtins.open", new_callable=mock_open, read_data='{"invalid": "format"}')
    def test_invalid_json_format(self, mock_file):
        result = load_transactions('bad_format.json')
        self.assertEqual(result, [])

    @patch("builtins.open", new_callable=mock_open, read_data='')
    def test_empty_file(self, mock_file):
        result = load_transactions('empty_file.json')
        self.assertEqual(result, [])



    class TestLoadTransactions(TestCase):

        @patch("os.path.exists", return_value=True)  # Замокаем проверку существования файла
        @patch("builtins.open", new_callable=mock_open, read_data='["item"]')
        def test_single_item_in_list(self, mock_open_func, mock_exists):
            result = load_transactions('single_item.json')

            # Проверяем, что open был вызван
            mock_open_func.assert_called_once()

            # Проверяем результат
            self.assertEqual(result, ["item"])


if __name__ == "__main__":
    unittest.main()