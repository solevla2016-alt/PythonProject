import unittest
import json
from unittest.mock import mock_open, patch
from src.utils import load_transactions



class TestLoadTransactions(unittest.TestCase):

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data="[]")
    def test_valid_empty_list(self, mock_open_func, mock_exists):
        """Тест: корректный пустой JSON-список."""
        result = load_transactions("test.json")
        self.assertEqual(result, [])
        mock_open_func.assert_called_once()

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='[{"id": 1, "amount": 100}]')
    def test_valid_list_of_dicts(self, mock_open_func, mock_exists):
        """Тест: корректный JSON со списком словарей."""
        result = load_transactions("test.json")
        expected = [{"id": 1, "amount": 100}]
        self.assertEqual(result, expected)
        mock_open_func.assert_called_once()

    @patch("os.path.exists", return_value=False)
    def test_file_not_found(self, mock_exists):
        """Тест: файл не существует."""
        result = load_transactions("missing.json")
        self.assertEqual(result, [])

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", side_effect=json.JSONDecodeError("Expecting value", "", 0))
    def test_invalid_json_format(self, mock_open_func, mock_exists):
        """Тест: некорректный JSON (ошибка декодирования)."""
        result = load_transactions("bad.json")
        self.assertEqual(result, [])
        mock_open_func.assert_called_once()

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data="")
    def test_empty_file(self, mock_open_func, mock_exists):
        """Тест: пустой файл (не JSON)."""
        result = load_transactions("empty.json")
        self.assertEqual(result, [])
        mock_open_func.assert_called_once()

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", new_callable=mock_open, read_data='{"not": "a list"}')
    def test_json_not_a_list(self, mock_open_func, mock_exists):
        """Тест: JSON — не список (например, словарь)."""
        result = load_transactions("not_list.json")
        self.assertEqual(result, [])
        mock_open_func.assert_called_once()

    @patch("os.path.exists", return_value=True)
    @patch("builtins.open", side_effect=PermissionError("Access denied"))
    def test_permission_error(self, mock_open_func, mock_exists):
        """Тест: ошибка прав доступа к файлу."""
        result = load_transactions("forbidden.json")
        self.assertEqual(result, [])
        mock_open_func.assert_called_once()



if __name__ == "__main__":
    unittest.main()
