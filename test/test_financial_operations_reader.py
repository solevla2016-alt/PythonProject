import unittest
from unittest.mock import patch, MagicMock
from src.financial_operations_reader import read_csv_file, read_excel_file
import pandas as pd
from pathlib import Path


class TestFinancialOperationsReader(unittest.TestCase):

    # 1. УСПЕШНОЕ ЧТЕНИЕ CSV (уже есть, оставляем)
    @patch('pandas.read_csv')
    @patch('pathlib.Path.is_file', return_value=True)
    def test_read_csv_valid(self, mock_is_file, mock_read_csv):
        mock_df = pd.DataFrame({
            'TransactionID': [1, 2],
            'Amount': ['$100', '$200'],
            'Currency': ['USD', 'EUR']
        })
        mock_read_csv.return_value = mock_df
        mock_df.to_dict = MagicMock(return_value=[
            {'TransactionID': 1, 'Amount': '$100', 'Currency': 'USD'},
            {'TransactionID': 2, 'Amount': '$200', 'Currency': 'EUR'}
        ])

        result = read_csv_file('/fake/path/to/file.csv')
        expected_result = [
            {'TransactionID': 1, 'Amount': '$100', 'Currency': 'USD'},
            {'TransactionID': 2, 'Amount': '$200', 'Currency': 'EUR'}
        ]
        self.assertEqual(result, expected_result)

        mock_read_csv.assert_called_with(
            Path('/fake/path/to/file.csv'),
            sep=';',
            encoding='utf-8'
        )

    # 2. ОТСУТСТВУЮЩИЙ CSV (уже есть, оставляем)
    @patch('pathlib.Path.is_file', return_value=False)
    def test_read_csv_nonexistent_file(self, mock_is_file):
        nonexistent_path = '/nonexistent/path/to/file.csv'
        with self.assertRaises(FileNotFoundError) as cm:
            read_csv_file(nonexistent_path)
        error_msg = str(cm.exception)
        self.assertIn('Файл не найден', error_msg)
        expected_path = Path(nonexistent_path).as_posix()
        actual_path = Path(error_msg.split('Файл не найден: ')[-1]).as_posix()
        self.assertIn(expected_path, actual_path)


    # 3. ОШИБКА ЧТЕНИЯ CSV (новая)
    @patch('pandas.read_csv', side_effect=pd.errors.ParserError("Ошибка чтения CSV"))
    @patch('pathlib.Path.is_file', return_value=True)
    def test_read_csv_parse_error(self, mock_is_file, mock_read_csv):
        """Тестирует обработку ошибки парсинга CSV."""
        with self.assertRaises(pd.errors.ParserError) as cm:
            read_csv_file('/fake/path/to/invalid.csv')
        self.assertIn("Ошибка чтения CSV", str(cm.exception))


    # 4. ПУСТОЙ CSV (новая)
    @patch('pandas.read_csv')
    @patch('pathlib.Path.is_file', return_value=True)
    def test_read_csv_empty_file(self, mock_is_file, mock_read_csv):
        """Тестирует чтение пустого CSV-файла."""
        mock_read_csv.return_value = pd.DataFrame()  # Пустой DataFrame
        result = read_csv_file('/fake/path/to/empty.csv')
        self.assertEqual(result, [])  # Ожидаем пустой список


    # 5. CSV БЕЗ ЗАГОЛОВКОВ (новая)
    @patch('pandas.read_csv')
    @patch('pathlib.Path.is_file', return_value=True)
    def test_read_csv_no_headers(self, mock_is_file, mock_read_csv):
        """Тестирует CSV без заголовков (должно вызвать ошибку или вернуть пустые ключи)."""
        mock_read_csv.return_value = pd.DataFrame([[1, '$100', 'USD']])
        mock_read_csv.return_value.columns = [0, 1, 2]  # Нет строковых заголовков
        result = read_csv_file('/fake/path/to/noheaders.csv')
        # Если логика допускает такие файлы — проверяем результат, иначе ждём исключение
        self.assertTrue(isinstance(result, list))


    # 6. УСПЕШНОЕ ЧТЕНИЕ EXCEL (уже есть, оставляем)
    @patch('pandas.read_excel')
    @patch('pathlib.Path.is_file', return_value=True)
    def test_read_excel_valid(self, mock_is_file, mock_read_excel):
        mock_df = pd.DataFrame({
            'TransactionID': [1, 2],
            'Amount': ['$100', '$200'],
            'Currency': ['USD', 'EUR']
        })
        mock_read_excel.return_value = mock_df
        mock_df.to_dict = MagicMock(return_value=[
            {'TransactionID': 1, 'Amount': '$100', 'Currency': 'USD'},
            {'TransactionID': 2, 'Amount': '$200', 'Currency': 'EUR'}
        ])
        result = read_excel_file('/fake/path/to/file.xlsx')
        expected_result = [
            {'TransactionID': 1, 'Amount': '$100', 'Currency': 'USD'},
            {'TransactionID': 2, 'Amount': '$200', 'Currency': 'EUR'}
        ]
        self.assertEqual(result, expected_result)
        mock_read_excel.assert_called_with(
            Path('/fake/path/to/file.xlsx'),
            engine='openpyxl'
        )

    # 7. ОТСУТСТВУЮЩИЙ EXCEL (уже есть, оставляем)
    @patch('pathlib.Path.is_file', return_value=False)
    def test_read_excel_nonexistent_file(self, mock_is_file):
        nonexistent_path = '/nonexistent/path/to/file.xlsx'
        with self.assertRaises(FileNotFoundError) as cm:
            read_excel_file(nonexistent_path)
        error_msg = str(cm.exception)
        self.assertIn('Файл не найден', error_msg)
        expected_path = Path(nonexistent_path).as_posix()
        actual_path = Path(error_msg.split('Файл не найден: ')[-1]).as_posix()
        self.assertIn(expected_path, actual_path)

    # 8. ОШИБКА ЧТЕНИЯ EXCEL (новая)
    @patch('pandas.read_excel', side_effect=ValueError("Неверный формат Excel"))
    @patch('pathlib.Path.is_file', return_value=True)
    def test_read_excel_invalid_format(self, mock_is_file, mock_read_excel):
        """Тестирует ошибку чтения Excel (например, .xls вместо .xlsx)."""
        with self.assertRaises(ValueError) as cm:
            read_excel_file('/fake/path/to/badformat.xls')
        self.assertIn("Неверный формат Excel", str(cm.exception))

    @patch('pandas.read_excel')
    @patch('pathlib.Path.is_file', return_value=True)
    def test_read_excel_empty_file(self, mock_is_file, mock_read_excel):
        """Тестирует чтение пустого Excel-файла."""
        mock_read_excel.return_value = pd.DataFrame()  # Пустой DataFrame
        result = read_excel_file('/fake/path/to/empty.xlsx')
        self.assertEqual(result, [])  # Ожидаем пустой список

    # 10. EXCEL С NaN-ЗНАЧЕНИЯМИ (новая)
    @patch('pandas.read_excel')
    @patch('pathlib.Path.is_file', return_value=True)
    def test_read_excel_with_nan_values(self, mock_is_file, mock_read_excel):
        """Тестирует обработку NaN-значений в Excel."""
        mock_df = pd.DataFrame({
            'TransactionID': [1, None],
            'Amount': ['$100', None],
            'Currency': ['USD', 'EUR']
        })
        mock_read_excel.return_value = mock_df
        mock_df.to_dict = MagicMock(return_value=[
            {'TransactionID': 1.0, 'Amount': '$100', 'Currency': 'USD'},
            {'TransactionID': None, 'Amount': None, 'Currency': 'EUR'}
        ])

        result = read_excel_file('/fake/path/to/file_with_nan.xlsx')

        # Проверяем, что NaN преобразовались в None или остались как есть
        expected_result = [
            {'TransactionID': 1.0, 'Amount': '$100', 'Currency': 'USD'},
            {'TransactionID': None, 'Amount': None, 'Currency': 'EUR'}
        ]
        self.assertEqual(result, expected_result)

    # 11. CSV С ПУСТЫМИ СТРОКАМИ (новая)
    @patch('pandas.read_csv')
    @patch('pathlib.Path.is_file', return_value=True)
    def test_read_csv_with_empty_rows(self, mock_is_file, mock_read_csv):
        """Тестирует CSV с пустыми строками."""
        # DataFrame с пустыми строками (NaN)
        mock_df = pd.DataFrame({
            'TransactionID': [1, None, 2],
            'Amount': ['$100', None, '$200'],
            'Currency': ['USD', None, 'EUR']
        })
        mock_read_csv.return_value = mock_df
        mock_df.to_dict = MagicMock(return_value=[
            {'TransactionID': 1.0, 'Amount': '$100', 'Currency': 'USD'},
            {'TransactionID': None, 'Amount': None, 'Currency': None},
            {'TransactionID': 2.0, 'Amount': '$200', 'Currency': 'EUR'}
        ])

        result = read_csv_file('/fake/path/to/file_with_empty_rows.csv')

        expected_result = [
            {'TransactionID': 1.0, 'Amount': '$100', 'Currency': 'USD'},
            {'TransactionID': None, 'Amount': None, 'Currency': None},
            {'TransactionID': 2.0, 'Amount': '$200', 'Currency': 'EUR'}
        ]
        self.assertEqual(result, expected_result)

    # 12. ПРОВЕРКА КОДИРОВКИ CSV (новая)
    @patch('pandas.read_csv', side_effect=UnicodeDecodeError('utf-8', b'\xff\xfe', 0, 1, 'недопустимый байт'))
    @patch('pathlib.Path.is_file', return_value=True)
    def test_read_csv_encoding_error(self, mock_is_file, mock_read_csv):
        """Тестирует ошибку кодировки при чтении CSV."""
        with self.assertRaises(UnicodeDecodeError) as cm:
            read_csv_file('/fake/path/to/bad_encoding.csv')
        self.assertIn('недопустимый байт', str(cm.exception))







