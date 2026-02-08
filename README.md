Проект по обработке финансовых данных
Описание
Проект предназначен для безопасной работы с финансовыми данными: маскировки платёжных реквизитов, фильтрации и сортировки транзакций, преобразования форматов даты.

Структура проекта
src/
├── mask.py          # Функции маскировки номеров карт и счетов
├── widget.py        # Обработка входных строк, преобразование даты
└── processing.py    # Фильтрация и сортировка транзакций
Установка
Клонируйте репозиторий:

bash
git clone <url-репозитория>
Перейдите в директорию проекта:

bash
cd <название-проекта>
Примечание: проект использует только встроенные модули Python, дополнительные зависимости не требуются.

Функционал и использование
1. Маскировка платёжных данных (src/mask.py)
get_mask_card_number(card_number: str) -> str
Маскирует номер карты по шаблону XXXX XX** **** XXXX.

Параметры:

card_number — номер карты (строка из 16 цифр).

Возвращает: маскированный номер или None при ошибке.

Пример:

python
from src.mask import get_mask_card_number
print(get_mask_card_number("7000792289606361"))  # 7000 79** **** 6361
get_mask_account(account_number: str) -> str
Маскирует номер счёта по шаблону **XXXX.

Параметры:

account_number — номер счёта (строка минимум из 4 цифр).

Возвращает: маскированный номер или None при ошибке.

Пример:

python
from src.mask import get_mask_account
print(get_mask_account("1234567890"))  # **7890
2. Обработка входных данных (src/widget.py)
mask_account_card(info_str: str) -> str
Автоматически определяет тип инструмента и применяет соответствующую маскировку.

Параметры:

info_str — входная строка с типом инструмента и номером.

Возвращает: маскированный номер или "None" при ошибке.

Примеры:

python
from src.widget import mask_account_card
print(mask_account_card("Visa Platinum 7000792289606361"))  # 7000 79** **** 6361
print(mask_account_card("счет 1234567890"))                   # **7890
print(mask_account_card("Unknown 1234"))                    # None
get_date(date_str: str) -> str
Преобразует дату из формата ISO 8601 в ДД.ММ.ГГГГ.

Параметры:

date_str — дата в формате ISO 8601.

Возвращает: дата в формате ДД.ММ.ГГГГ.

Пример:

python
from src.widget import get_date
print(get_date("2024-03-11T02:26:18.671407"))  # 11.03.2024
3. Обработка транзакций (src/processing.py)
filter_by_state(dict_lists: list, state: str = "EXECUTED") -> list
Фильтрует список транзакций по статусу.

Параметры:

dict_lists — список словарей с транзакциями;

state — статус для фильтрации (по умолчанию "EXECUTED").

Возвращает: список транзакций с указанным статусом.

Пример:

python
from src.processing import filter_by_state

data = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]

filtered = filter_by_state(data, "CANCELED")
print(filtered)  # Только транзакции со статусом "CANCELED"
sort_by_date(transactions: list, reverse: bool = True) -> list
Сортирует транзакции по дате.

Параметры:

transactions — список транзакций;

reverse — порядок сортировки (True — по убыванию, False — по возрастанию; по умолчанию True).

Возвращает: отсортированный список транзакций.

Пример:

python
from src.processing import sort_by_date

data = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
]

sorted_data = sort_by_date(data, reverse=False)
print(sorted_data)  # Сортировка по возрастанию даты
Полный пример использования
python
from src.mask import get_mask_card_number, get_mask_account
from src.widget import mask_account_card, get_date
from src.processing import filter_by_state, sort_by_date

# Маскировка номеров
print(get_mask_card_number("7000792289606361"))  # 7000 79** **** 6361
print(get_mask_account("1234567890"))               # **7890

# Автоматическое определение и маскировка
print(mask_account_card("Visa Platinum 7000792289606361"))

# Преобразование даты
print(get_date("2024-03-11T02:26:18.671407"))  # 11.03.2024

# Фильтрация и сортировка транзакций
transactions = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]

filtered = filter_by_state(transactions, "EXECUTED")
sorted_transactions = sort_by_date(transactions, reverse=True)

print(filtered)
print(sorted_transactions)
Требования
Python 3.6 или выше;

Нет внешних зависимостей (используются только встроенные модули).

Лицензия
Проект распространяется под лицензией MIT.

mport functools
from datetime import datetime
from typing import Any, Callable, Optional


def _get_timestamp() -> str:
    """Возвращает текущую дату и время в формате YYYY-MM-DD HH:MM:SS."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(filename: Optional[str] = None) -> Callable:
    """
    Декоратор для логирования вызова функции (успех/ошибка) в файл или консоль.

    Args:
        filename (str, optional): Путь к файлу для логирования. Если None — вывод в консоль.
    Returns:
        Callable: Декоратор, оборачивающий функцию.
    """

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Обёртка, добавляющая логирование вызова функции."""
            try:
                result = func(*args, **kwargs)
                message = f"{func.__name__} ok"

                if filename:
                    with open(filename, mode="a", encoding="utf-8") as file:
                        file.write(f"[{_get_timestamp()}] {message}\n")
                else:
                    print(message)

                return result

            except (KeyboardInterrupt, SystemExit):
                raise
            except Exception as e:
                err_message = (
                    f"{func.__name__}: error: {type(e).__name__}. "
                    f"Inputs: {args}, {kwargs}"
                )

                if filename:
                    try:
                        with open(filename, mode="a", encoding="utf-8") as file:
                            file.write(f"[{_get_timestamp()}] {err_message}\n")
                    except OSError as log_error:
                        print(f"Log write error: {log_error}")
                else:
                    print(err_message)

                raise e

        return wrapper

    return decorator

import pytest
import os
from src.decorators import log

class TestLogDecorator:
    def setup_method(self):
        self.test_file_name = "test_log.txt"
        if os.path.exists(self.test_file_name):
            os.remove(self.test_file_name)


    def teardown_method(self):
        if os.path.exists(self.test_file_name):
            os.remove(self.test_file_name)

    def test_successful_execution_console_output(self, capsys):
        """Тестируем успешное выполнение функции с выводом в консоль"""
        @log()
        def successful_func():
            return "OK"

        successful_func()

        captured = capsys.readouterr()
        assert "successful_func ok" in captured.out

    def test_error_handling_console_output(self, capsys):
        """Тестируем возникновение ошибки с выводом в консоль"""
        @log()
        def failing_func():
            raise ValueError("Test Error")

        with pytest.raises(ValueError):
            failing_func()

        captured = capsys.readouterr()
        assert "failing_func: error: ValueError" in captured.out
        assert "Inputs: (), {}" in captured.out

    def test_successful_execution_file_logging(self):
        """Тестируем успешное выполнение функции с логированием в файл"""
        @log(filename=self.test_file_name)
        def successful_func():
            return "ok"

        successful_func()

        with open(self.test_file_name, 'r', encoding='utf-8') as file:
            content = file.read().strip()

        assert "successful_func ok" in content

    def test_error_handling_file_logging(self):
        """Тестируем возникновение ошибки с логированием в файл"""
        @log(filename=self.test_file_name)
        def failing_func():
            raise TypeError("Test Error")

        with pytest.raises(TypeError):
            failing_func()

        with open(self.test_file_name, 'r', encoding='utf-8') as file:
            content = file.read().strip()


        assert "failing_func: error: TypeError" in content
        assert "Inputs: (), {}" in content


Скопируйте .env.example в .env:

bash
cp .env.example .env
Заполните .env своими реальными ключами и настройками.

import json
import os
from typing import Any, Dict, List


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает список словарей с данными о финансовых транзакциях из JSON‑файла.

    """
    try:
        if not os.path.exists(file_path):
            print(f"[DEBUG] Файл не найден: {file_path}")
            return []

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            print(f"[DEBUG] Загружено из файла: {data}")

        if isinstance(data, list):
            return data
        else:
            print(f"[DEBUG] Данные не являются списком (тип: {type(data)})")
            return []

    except FileNotFoundError:
        print(f"[DEBUG] FileNotFoundError: файл не найден — {file_path}")
        return []

    except PermissionError:
        print(f"[DEBUG] PermissionError: нет доступа к файлу — {file_path}")
        return []

    except json.JSONDecodeError as e:
        print(f"[DEBUG] JSONDecodeError: ошибка парсинга JSON — {e}")
        return []

    except UnicodeDecodeError as e:
        print(f"[DEBUG] UnicodeDecodeError: ошибка кодировки файла — {e}")
        return []

    except Exception as e:
        print(f"[DEBUG] Неожиданная ошибка: {type(e).__name__}: {e}")
        return []

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

import os
from functools import lru_cache
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()

# Получение и проверка API_KEY
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY не найден в .env. Создайте файл .env с API_KEY=ваш_ключ.")


BASE_URL = "https://api.apilayer.com/exchangerates_data/convert"


@lru_cache(maxsize=128)
def _get_exchange_rate(from_currency: str, to_currency: str) -> float:
    """Получает курс конвертации с кешированием."""
    params = {"from": from_currency, "to": to_currency, "amount": str(1)}
    headers = {"apikey": API_KEY}

    for attempt in range(2):
        try:
            response = requests.get(
                BASE_URL, params=params, headers=headers, timeout=10
            )
            response.raise_for_status()
            data = response.json()

            if isinstance(data, dict) and "error" in data:
                error_info = data["error"].get("info", "Неизвестная ошибка")
                raise Exception(f"API ошибка: {error_info}")
            elif not isinstance(data, dict):
                raise Exception("Неверный формат ответа API")

            return float(data["result"])

        except requests.exceptions.RequestException as e:
            if attempt == 1:
                raise Exception(f"Ошибка запроса к API после 2 попыток: {e}")
            continue

    raise Exception("Не удалось получить курс конвертации после 2 попыток")


def convert_to_rubles(amount: float, currency: str) -> float:
    """Конвертирует сумму из валюты в RUB через APILayer."""
    try:
        rate = _get_exchange_rate(currency, "RUB")
        converted = amount * rate
        return round(converted, 2)
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Сетевой сбой при запросе курса {currency}→RUB: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Ошибка получения курса {currency}→RUB: {e}") from e


def process_transaction(transaction: Dict[str, Any]) -> float:
    """Обрабатывает транзакцию и возвращает сумму в рублях."""

    # Проверка наличия обязательных ключей
    if "operationAmount" not in transaction:
        raise KeyError("Поле 'operationAmount' отсутствует в транзакции.")

    if "amount" not in transaction["operationAmount"]:
        raise KeyError("Поле 'operationAmount.amount' отсутствует в транзакции.")
    if "currency" not in transaction["operationAmount"]:
        raise KeyError("Поле 'operationAmount.currency' отсутствует в транзакции.")
    if "code" not in transaction["operationAmount"]["currency"]:
        raise KeyError("Поле 'operationAmount.currency.code' отсутствует в транзакции.")

    # Извлечение данных
    amount_value = transaction["operationAmount"]["amount"]
    currency_code = transaction["operationAmount"]["currency"]["code"]

    # Валидация amount
    if isinstance(amount_value, (int, float)):
        amount = float(amount_value)
    elif isinstance(amount_value, str):
        amount_str = amount_value.strip()
        if not amount_str:
            raise ValueError(
                "Поле 'operationAmount.amount' не может быть пустой строкой."
            )
        try:
            amount = float(amount_str)
        except ValueError:
            raise ValueError(
                f"Поле 'operationAmount.amount' должно быть числом, получено: {amount_value}"
            )
    else:
        raise TypeError(
            f"Поле 'operationAmount.amount' должно быть числом или строкой, получено: {type(amount_value).__name__}"
        )

    if amount < 0:
        raise ValueError(
            f"Поле 'operationAmount.amount' не может быть отрицательным: {amount}"
        )

    # Валидация currency.code
    if not isinstance(currency_code, str):
        raise TypeError(
            f"Поле 'operationAmount.currency.code' должно быть строкой, получено: {type(currency_code).__name__}"
        )

    currency = currency_code.strip().upper()
    if not currency:
        raise ValueError(
            "Поле 'operationAmount.currency.code' не может быть пустой строкой."
        )

    SUPPORTED_CURRENCIES = {"RUB", "USD", "EUR"}
    if currency not in SUPPORTED_CURRENCIES:
        raise ValueError(
            f"Валюта {currency} не поддерживается. Используйте: {SUPPORTED_CURRENCIES}."
        )

    return convert_to_rubles(amount, currency)

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

import pytest
from src.mask import get_mask_card_number, get_mask_account



def test_get_mask_card_number_valid():
    """Тест: корректная маскировка 16‑значной карты."""
    result = get_mask_card_number("1234567890123456")
    assert result == "1234 56** **** 3456"




def test_get_mask_card_number_invalid_length_short():
    """Тест: номер карты короче 16 цифр."""
    result = get_mask_card_number("123456789012345")
    assert result == ""



def test_get_mask_card_number_non_digit():
    """Тест: в номере карты есть нецифровые символы."""
    result = get_mask_card_number("abcd567890123456")
    assert result == ""



def test_get_mask_card_number_too_long():
    """Тест: номер карты длиннее 16 цифр."""
    result = get_mask_card_number("12345678901234567")
    assert result == ""



def test_get_mask_card_number_minimum_length():
    """Тест: минимальная допустимая длина (16 цифр)."""
    result = get_mask_card_number("1234567890123456")
    assert result == "1234 56** **** 3456"

def test_get_mask_account_empty_string():
    """Тест: пустой номер счёта."""
    result = get_mask_account("")
    assert result == ""



def test_get_mask_account_non_digit_chars():
    """Тест: номер счёта с буквами."""
    result = get_mask_account("abc123")
    assert result == ""



def test_get_mask_account_whitespace():
    """Тест: номер счёта с пробелами."""
    result = get_mask_account(" 1234 ")
    assert result == ""



@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("1234567890123456", "1234 56** **** 3456"),
        ("4444444444444444", "4444 44** **** 4444"),
        ("9999999999999999", "9999 99** **** 9999"),
    ],
)
def test_get_mask_card_number_parametrized(card_number, expected):
    """Параметризованный тест для маскировки номера карты."""
    result = get_mask_card_number(card_number)
    assert result == expected

from pathlib import Path

import pandas as pd


def read_csv_file(file_path: str) -> list:
    """Читает CSV и возвращает список словарей."""
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"Файл не найден: {path.absolute()}")

    df = pd.read_csv(path, sep=";", encoding="utf-8")
    return df.to_dict("records")


def read_excel_file(file_path: str) -> list:
    """Читает Excel и возвращает список словарей."""
    path = Path(file_path)

    if not path.is_file():
        raise FileNotFoundError(f"Файл не найден: {path.absolute()}")

    df = pd.read_excel(path, engine="openpyxl")
    return df.to_dict("records")


if __name__ == "__main__":
    project_root = Path(__file__).parent.parent
    csv_path = project_root / "data" / "transactions.csv"
    excel_path = project_root / "data" / "transactions_excel.xlsx"

    try:
        csv_data = read_csv_file(str(csv_path))
        excel_data = read_excel_file(str(excel_path))

        print("Первые 2 записи из CSV:", csv_data[:2])
        print("Первые 2 записи из Excel:", excel_data[:2])

    except Exception as e:
        print(f"Ошибка: {e}")

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


import csv
import json
from datetime import date, datetime, time, timedelta
from typing import Any, Dict, List

from openpyxl import load_workbook
from openpyxl.worksheet.worksheet import Worksheet


def load_json_transactions(file_path: str) -> List[Dict[str, Any]]:
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
        if not isinstance(data, list):
            raise ValueError("JSON должен содержать список транзакций")
        return data


def load_csv_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Загрузка транзакций из CSV-файла."""
    transactions = []
    with open(file_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            transactions.append(row)
    return transactions


def _normalize_cell_value(value: Any) -> Any:
    if value is None:
        return None
    if isinstance(value, date) or isinstance(value, datetime):
        return value.isoformat()
    elif isinstance(value, time):
        return value.strftime("%H:%M:%S")
    elif isinstance(value, timedelta):
        return str(value)
    elif hasattr(value, "text"):
        return str(value.text)
    return value


def load_xlsx_transactions(filepath: str) -> List[Dict[str, Any]]:
    wb = load_workbook(filepath)
    sheet = wb.active

    if sheet is None:
        raise ValueError("Активный лист не найден")
    if not isinstance(sheet, Worksheet):
        raise TypeError(f"Лист имеет тип {type(sheet)}, а не Worksheet")

    headers = [str(cell.value) if cell.value is not None else "" for cell in sheet[1]]

    transactions: List[Dict[str, Any]] = []

    for row in sheet.iter_rows(min_row=2):
        transaction: Dict[str, Any] = {}
        for idx, cell in enumerate(row):
            if idx < len(headers):
                key = headers[idx]
                raw_value = cell.value
                normalized_value = _normalize_cell_value(raw_value)
                transaction[key] = normalized_value
        transactions.append(transaction)

    return transactions


def filter_by_status(
    transactions: List[Dict[str, Any]], status: str
) -> List[Dict[str, Any]]:
    """Фильтрация транзакций по статусу (с приведением к верхнему регистру)."""
    return [t for t in transactions if t.get("state", "").upper() == status.upper()]


def sort_transactions(
    transactions: List[Dict[str, Any]], ascending: bool = True
) -> List[Dict[str, Any]]:
    """Сортировка транзакций по дате."""
    return sorted(
        transactions,
        key=lambda x: datetime.strptime(x["date"], "%d.%m.%Y"),
        reverse=not ascending,
    )


def filter_ruble_transactions(
    transactions: List[Dict[str, Any]],
) -> List[Dict[str, Any]]:
    """Фильтрация транзакций только в рублях."""
    ruble_variants = ["руб", "rub", "rur"]  # Поддерживаем разные написания
    return [
        t
        for t in transactions
        if (
            t.get("operationAmount", {}).get("currency", {}).get("name", "").lower()
            in ruble_variants
        )
    ]


def search_by_keyword(
    transactions: List[Dict[str, Any]], keyword: str
) -> List[Dict[str, Any]]:
    """Поиск транзакций по ключевому слову в описании."""
    return [
        t
        for t in transactions
        if keyword.lower() in str(t.get("description", "")).lower()
    ]


def print_transactions(transactions: List[Dict[str, Any]]) -> None:
    """Вывод транзакций в консоль."""
    if not transactions:
        print("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")
        return

    print(f"\nВсего банковских операций в выборке: {len(transactions)}\n")
    for t in transactions:
        date = t.get("date", "")
        description = t.get("description", "")
        from_acc = t.get("from", "")
        to_acc = t.get("to", "")

        # Получаем сумму и валюту
        op_amount = t.get("operationAmount", {})
        amount = op_amount.get("amount", "")
        currency = op_amount.get("currency", {}).get("name", "")

        print(f"{date} {description}")

        if from_acc:
            print(f"{from_acc} -> {to_acc}")
        else:
            # Маскируем последние 4 цифры счёта ВСЕГДА (даже если короткий)
            to_str = str(to_acc) if to_acc else ""
            if len(to_str) >= 4:
                print(f"Счет **{to_str[-4:]}")
            else:
                # Если меньше 4 цифр — выводим как есть, но с префиксом "Счет **"
                print(f"Счет **{to_str}")

        print(f"Сумма: {amount} {currency}\n")


def main() -> None:
    print("Привет! Добро пожаловать в программу работы с банковскими транзакциями.")
    print("Выберите необходимый пункт меню:")
    print("1. Получить информацию о транзакциях из JSON-файла")
    print("2. Получить информацию о транзакциях из CSV-файла")
    print("3. Получить информацию о транзакциях из XLSX-файла")

    choice = input("> ")

    if choice == "1":
        print("Для обработки выбран JSON-файл.")
        file_path = input("Введите путь к JSON-файлу: ")
        transactions = load_json_transactions(file_path)
    elif choice == "2":
        print("Для обработки выбран CSV-файл.")
        file_path = input("Введите путь к CSV-файлу: ")
        transactions = load_csv_transactions(file_path)
    elif choice == "3":
        print("Для обработки выбран XLSX-файл.")
        file_path = input("Введите путь к XLSX-файлу: ")
        transactions = load_xlsx_transactions(file_path)
    else:
        print("Неверный выбор. Завершение программы.")
        return

    valid_statuses = ["EXECUTED", "CANCELED", "PENDING"]
    status = ""
    while True:
        print("Введите статус, по которому необходимо выполнить фильтрацию.")
        print(f"Доступные для фильтровки статусы: {', '.join(valid_statuses)}")
        status = input("> ").strip()
        if status.upper() in valid_statuses:
            break
        else:
            print(f'Статус операции "{status}" недоступен.')

    print(f'Операции отфильтрованы по статусу "{status.upper()}"')
    filtered_transactions = filter_by_status(transactions, status)

    sort_choice = input("Отсортировать операции по дате? Да/Нет\n> ").strip().lower()
    if sort_choice == "да":
        order = (
            input("Отсортировать по возрастанию или по убыванию?\n> ").strip().lower()
        )
        ascending = order == "по возрастанию"
        filtered_transactions = sort_transactions(filtered_transactions, ascending)

    ruble_choice = (
        input("Выводить только рублёвые транзакции? Да/Нет\n> ").strip().lower()
    )
    if ruble_choice == "да":
        filtered_transactions = filter_ruble_transactions(filtered_transactions)

    keyword_choice = (
        input(
            "Отфильтровать список транзакций по определённому слову в описании? Да/Нет\n> "
        )
        .strip()
        .lower()
    )
    if keyword_choice == "да":
        keyword = input("Введите ключевое слово: ").strip()
        filtered_transactions = search_by_keyword(filtered_transactions, keyword)

    print("Распечатываю итоговый список транзакций...")
    print_transactions(filtered_transactions)


if __name__ == "__main__":
    main()


import unittest
from unittest.mock import mock_open, patch, MagicMock
from datetime import datetime, time, timedelta



# Импортируем функции из main.py
from src.main import (
    load_json_transactions,
    load_csv_transactions,
    load_xlsx_transactions,
    filter_by_status,
    sort_transactions,
    filter_ruble_transactions,
    search_by_keyword,
    print_transactions,
    main,
    _normalize_cell_value
)


class TestTransactionFunctions(unittest.TestCase):

    def setUp(self):
        """Подготавливаем тестовые данные с корректной структурой."""
        self.transactions = [
            {
                "date": "08.12.2019",
                "description": "Открытие вклада",
                "to": "4321",
                "operationAmount": {
                    "amount": "40542",
                    "currency": {"name": "руб"}
                },
                "state": "EXECUTED"
            },
            {
                "date": "12.11.2019",
                "description": "Перевод с карты на карту",
                "from": "MasterCard 7771 27** **** 3727",
                "to": "Visa Platinum 1293 38** **** 9203",
                "operationAmount": {
                    "amount": "130",
                    "currency": {"name": "USD"}
                },
                "state": "CANCELED"
            },
            {
                "date": "18.07.2018",
                "description": "Перевод организации",
                "from": "Visa Platinum 7492 65** **** 7202",
                "to": "0034",
                "operationAmount": {
                    "amount": "8390",
                    "currency": {"name": "руб"}
                },
                "state": "EXECUTED"
            }
        ]

    # --- Тесты загрузки данных ---

    @patch("builtins.open", new_callable=mock_open, read_data='[{"state": "EXECUTED"}]')
    def test_load_json_transactions(self, mock_file):
        result = load_json_transactions("dummy.json")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["state"], "EXECUTED")

    @patch("builtins.open", new_callable=mock_open, read_data="state,amount\nEXECUTED,100")
    def test_load_csv_transactions(self, mock_file):
        result = load_csv_transactions("dummy.csv")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["state"], "EXECUTED")
        self.assertEqual(result[0]["amount"], "100")

    class TestTransactionFunctions(unittest.TestCase):

        @patch("openpyxl.load_workbook") # ← критично: путь к функции в ВАШЕМ модуле
        def test_load_xlsx_transactions(self, mock_load_workbook):
            # 1. Настраиваем мок для рабочей книги
            mock_wb = MagicMock()
            mock_sheet = MagicMock()
            mock_wb.active = mock_sheet
            mock_load_workbook.return_value = mock_wb  # ← мок возвращает наш mock_wb

            # 2. Имитируем ячейки Excel
            class MockCell:
                def __init__(self, value):
                    self.value = value

            headers = [
                MockCell("date"),
                MockCell("state"),
                MockCell("operationAmount")
            ]
            data_row = [
                MockCell("01.01.2020"),
                MockCell("EXECUTED"),
                MockCell('{"amount": "1000", "currency": {"name": "руб"}}')
            ]

            # 3. Настраиваем поведение моков
            mock_sheet.__getitem__.return_value = headers
            mock_sheet.iter_rows.return_value = iter([data_row])

            # 4. Вызываем тестируемую функцию
            result = load_xlsx_transactions("dummy.xlsx")

            # 5. Проверки
            self.assertEqual(len(result), 1)
            self.assertIn("date", result[0])
            self.assertIn("state", result[0])
            self.assertEqual(result[0]["date"], "01.01.2020")
            self.assertEqual(result[0]["state"], "EXECUTED")
            self.assertIn("operationAmount", result[0])
            self.assertEqual(result[0]["operationAmount"]["amount"], "1000")
            self.assertEqual(
                result[0]["operationAmount"]["currency"]["name"],
                "руб"
            )
    # --- Тесты фильтрации и обработки ---

    def test_filter_by_status_case_insensitive(self):
        """Проверяем фильтрацию по статусу с игнорированием регистра."""
        result = filter_by_status(self.transactions, "executed")
        self.assertEqual(len(result), 2)
        self.assertTrue(all(t["state"] == "EXECUTED" for t in result))

    def test_sort_transactions_ascending(self):
        """Сортировка по дате (возрастание)."""
        result = sort_transactions(self.transactions, ascending=True)
        dates = [t["date"] for t in result]
        expected = ["18.07.2018", "12.11.2019", "08.12.2019"]
        self.assertEqual(dates, expected)

    def test_sort_transactions_descending(self):
        """Сортировка по дате (убывание)."""
        result = sort_transactions(self.transactions, ascending=False)
        dates = [t["date"] for t in result]
        expected = ["08.12.2019", "12.11.2019", "18.07.2018"]
        self.assertEqual(dates, expected)

    def test_filter_ruble_transactions(self):
        """Фильтрация только рублёвых транзакций."""
        result = filter_ruble_transactions(self.transactions)
        self.assertEqual(len(result), 2)
        self.assertTrue(all(
            t["operationAmount"]["currency"]["name"].lower() in ["руб", "rub", "rur"]
            for t in result
        ))

    def test_search_by_keyword(self):
        """Поиск по ключевому слову в описании."""
        result = search_by_keyword(self.transactions, "вклад")
        self.assertEqual(len(result), 1)
        self.assertIn("вклад", result[0]["description"].lower())

        result = search_by_keyword(self.transactions, "перевод")
        self.assertEqual(len(result), 2)

    # --- Тесты вывода ---

    def test_print_transactions_empty(self):
        """Вывод для пустого списка."""
        with patch("builtins.print") as mock_print:
            print_transactions([])
            mock_print.assert_any_call("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")

    def test_print_transactions_non_empty(self):
        """Вывод непустого списка транзакций."""
        with patch("builtins.print") as mock_print:
            print_transactions(self.transactions[:1])

            # Проверяем ключевые строки вывода
            mock_print.assert_any_call("\nВсего банковских операций в выборке: 1\n")
            mock_print.assert_any_call("08.12.2019 Открытие вклада")
            mock_print.assert_any_call("Счет **4321")
            mock_print.assert_any_call("Сумма: 40542 руб\n")

    # --- Тест main() ---

    def test_main_with_ruble_filter(self):
        """Полный сценарий: загрузка, фильтрация по статусу и валюте."""
        transactions = [
            {
                "id": 1,
                "state": "EXECUTED",
                "date": "2023-01-01T12:00:00",
                "operationAmount": {
                    "amount": "1000.00",
                    "currency": {"name": "руб"}
                },
                "description": "Перевод",
                "from": "Счёт 1234",
                "to": "Счёт 567"
            },
            {
                "id": 2,
                "state": "EXECUTED",
                "date": "2023-01-02T13:00:00",
                "operationAmount": {
                    "amount": "2500.50",
                    "currency": {"name": "руб"}
                },
                "description": "Оплата",
                "from": "Карта 9999",
                "to": "Магазин X"
            },
            {
                "id": 3,
                "state": "EXECUTED",
                "date": "2023-01-03T14:00:00",
                "operationAmount": {
                    "amount": "100.00",
                    "currency": {"name": "USD"}
                },
                "description": "Обмен валюты",
                "from": "Счёт 1111",
                "to": "Банк Y"
            }
        ]

        user_inputs = [
            "1",  # выбор JSON
            "test.json",  # путь к файлу
            "EXECUTED",  # статус для фильтрации
            "нет",  # не сортировать
            "да",  # фильтровать по валюте
            "руб",  # валюта
            "нет"  # не искать по ключевому слову
        ]

        with patch("builtins.input", side_effect=user_inputs):
            with patch("src.main.print_transactions") as mock_print:
                with patch("src.main.load_json_transactions") as mock_load_json:
                    mock_load_json.return_value = transactions

                    print("[ТЕСТ] Начальные транзакции (из load_json_transactions):")
                    for t in transactions:
                        print(
                            f"  ID {t['id']}, статус: {t['state']}, валюта: {t['operationAmount']['currency']['name']}")

                    main()

                    assert mock_print.call_count >= 1, "print_transactions не вызван!"
                    printed_transactions = mock_print.call_args_list[-1][0][0]

                    print(f"[ТЕСТ] Транзакции, переданные в print_transactions: {len(printed_transactions)}")
                    for t in printed_transactions:
                        print(f"  ID {t['id']}, валюта: {t['operationAmount']['currency']['name']}")

                    # Основные проверки
                    assert len(printed_transactions) == 2, (
                        f"Ожидалось 2 рублёвые транзакции, но получено {len(printed_transactions)}"
                    )

                    for t in printed_transactions:
                        assert t["operationAmount"]["currency"]["name"].lower() == "руб", (
                            f"Транзакция ID {t['id']} имеет валюту {t['operationAmount']['currency']['name']}"
                        )

    def test_main_with_keyword_search(self):
        """Тест main() с поиском по ключевому слову."""
        transactions = [
            {
                "id": 1,
                "state": "EXECUTED",
                "date": "2023-01-01T12:00:00",
                "operationAmount": {
                    "amount": "1000.00",
                    "currency": {"name": "руб"}
                },
                "description": "Перевод другу",
                "from": "Счёт 1234",
                "to": "Счёт 5678"
            },
            {
                "id": 2,
                "state": "EXECUTED",
                "date": "2023-01-02T13:00:00",
                "operationAmount": {
                    "amount": "500.00",
                    "currency": {"name": "руб"}
                },
                "description": "Оплата интернета",
                "from": "Карта 9999",
                "to": "Ростелеком"
            }
        ]

        user_inputs = [
            "1", "test.json", "EXECUTED", "нет", "нет", "да", "интернет"
        ]

        with patch("builtins.input", side_effect=user_inputs):
            with patch("src.main.print_transactions") as mock_print:
                with patch("src.main.load_json_transactions") as mock_load_json:
                    mock_load_json.return_value = transactions
                    main()

                    printed_transactions = mock_print.call_args_list[-1][0][0]
                    assert len(printed_transactions) == 1
                    assert "интернет" in printed_transactions[0]["description"].lower()

    def test_main_invalid_choice(self):
        """Тест на неверный выбор формата файла."""
        user_inputs = ["4"]  # неверный пункт меню

        with patch("builtins.input", side_effect=user_inputs):
            with patch("builtins.print") as mock_print:
                main()
                mock_print.assert_any_call("Неверный выбор. Завершение программы.")

    def test_load_json_transactions_not_list(self):
        """JSON содержит не список, а объект — должно вызвать ValueError."""
        with patch("builtins.open", mock_open(read_data='{"key": "value"}')):
            with self.assertRaises(ValueError) as cm:
                load_json_transactions("not_list.json")
            self.assertIn("JSON должен содержать список транзакций", str(cm.exception))

    def test_load_csv_transactions_empty_file(self):
        """Пустой CSV-файл (только заголовки или пусто)."""
        with patch("builtins.open", mock_open(read_data="date,description\n")):
            result = load_csv_transactions("empty.csv")
            self.assertEqual(len(result), 0)

    def test_load_csv_transactions_missing_columns(self):
        """CSV без некоторых ожидаемых колонок."""
        data = "state,amount\nEXECUTED,100"
        with patch("builtins.open", mock_open(read_data=data)):
            result = load_csv_transactions("partial.csv")
            self.assertIn("state", result[0])
            self.assertIn("amount", result[0])
            # Другие поля будут отсутствовать — это нормально

    def test_filter_by_status_missing_state_key(self):
        """Транзакция без поля 'state' — не должна попасть в результат."""
        transactions = [
            {"date": "01.01.2020", "description": "Test"},  # нет state
            {"date": "02.01.2020", "state": "EXECUTED", "description": "OK"}
        ]
        result = filter_by_status(transactions, "EXECUTED")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["state"], "EXECUTED")

    def test_sort_transactions_invalid_date_format(self):
        """Сортировка при невалидном формате даты — должна пропускать или поднимать ошибку."""
        transactions = [
            {"date": "не дата", "description": "Bad"},
            {"date": "01.01.2020", "description": "Good"}
        ]
        # Ожидается, что исключение поднимется при попытке парсинга
        with self.assertRaises(ValueError):
            sort_transactions(transactions, ascending=True)

    def test_filter_ruble_transactions_case_insensitive(self):
        """Фильтрация по валюте с разными регистрами."""
        transactions = [
            {
                "operationAmount": {"currency": {"name": "RUB"}}
            },
            {
                "operationAmount": {"currency": {"name": "rub"}}
            },
            {
                "operationAmount": {"currency": {"name": "RUR"}}
            },
            {
                "operationAmount": {"currency": {"name": "USD"}}
            }
        ]
        result = filter_ruble_transactions(transactions)
        self.assertEqual(len(result), 3)

    def test_search_by_keyword_case_insensitive(self):
        """Поиск по ключевому слову с разным регистром."""
        result = search_by_keyword(self.transactions, "ПЕРЕВОД")
        self.assertEqual(len(result), 2)  # оба перевода найдены

    def test_search_by_keyword_no_match(self):
        """Ключевое слово не найдено — пустой результат."""
        result = search_by_keyword(self.transactions, "ипотека")
        self.assertEqual(len(result), 0)

    def test_search_by_keyword_missing_description(self):
        """Транзакция без описания — не вызывает ошибки."""
        transactions = [
            {"id": 1},  # нет description
            {"id": 2, "description": "платеж"}
        ]
        result = search_by_keyword(transactions, "платеж")
        self.assertEqual(len(result), 1)

    def test_print_transactions_with_missing_fields(self):
        """Вывод транзакции с отсутствующими полями (from, to, amount и т.п.)."""
        transaction = {
            "date": "01.01.2020",
            "description": "Тест",
            # отсутствуют: from, to, operationAmount
        }
        with patch("builtins.print") as mock_print:
            print_transactions([transaction])

            mock_print.assert_any_call("01.01.2020 Тест")
            mock_print.assert_any_call("Сумма:  \n")  # amount и currency пустые

    def test_normalize_cell_value_datetime(self):
        """_normalize_cell_value: преобразование datetime в ISO-строку."""
        dt = datetime(2020, 1, 1, 12, 30, 45)
        self.assertEqual(_normalize_cell_value(dt), "2020-01-01T12:30:45")

    def test_normalize_cell_value_time(self):
        """_normalize_cell_value: преобразование time в HH:MM:SS."""
        t = time(12, 30, 45)
        self.assertEqual(_normalize_cell_value(t), "12:30:45")

    def test_normalize_cell_value_timedelta(self):
        """_normalize_cell_value: timedelta → строка."""
        td = timedelta(hours=1, minutes=30)
        self.assertEqual(_normalize_cell_value(td), "1:30:00")
    if __name__ == "__main__":
        unittest.main()




import re
from collections import Counter
from typing import Any, Dict, List


def process_bank_search(
    transactions: List[Dict[str, Any]], query: str
) -> List[Dict[str, Any]]:
    """Фильтрует список банковских транзакций по поисковому запросу в описании"""
    if not query:
        return transactions
    pattern = re.escape(query)
    compiled = re.compile(pattern, re.IGNORECASE)
    return [t for t in transactions if compiled.search(t.get("description", ""))]

def process_bank_operations(
    transactions: List[Dict[str, Any]], categories: List[str]
) -> Dict[str, int]:
    """Подсчитывает количество транзакций по заданным категориям."""
    counter: Counter[str] = Counter()  # Явная аннотация типа

    for transaction in transactions:
        desc = transaction.get("description", "").lower()

        for category in categories:
            if category.lower() in desc:
                counter[category] += 1

    return dict(counter)  

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

from datetime import datetime
from pathlib import Path
from typing import Any, Dict, List, Optional

import pandas as pd

from src.financial_operations_reader import read_csv_file
from src.processing import filter_by_state, sort_by_date
from src.utils import load_transactions


def _to_float(value: Any) -> Optional[float]:
    if value is None:
        return None
    if isinstance(value, (int, float)):
        return float(value)

    s = str(value).strip()
    if not s:
        return None
    s = s.replace(" ", "").replace(",", ".")
    try:
        return float(s)
    except (ValueError, TypeError):
        return None


def format_amount(value: float) -> str:
    if value is None:
        return ""
    if float(value).is_integer():
        return str(int(value))
    s = f"{value:.2f}"
    s = s.rstrip("0").rstrip(".")
    return s


def currency_label(code: str, name: str) -> str:
    c = (code or "").strip().upper()
    n = (name or "").strip()

    if c == "RUB":
        return "руб."
    if c:
        return c
    if n:
        return n
    return "N/A"


def mask_account_card(info_str: str) -> str:
    if not isinstance(info_str, str) or not info_str.strip():
        return "None"

    s = info_str.strip()
    first_digit_idx = None
    for i, ch in enumerate(s):
        if ch.isdigit():
            first_digit_idx = i
            break
    if first_digit_idx is None:
        return "None"

    type_part_raw = s[:first_digit_idx].strip()
    number_part = s[first_digit_idx:]
    cleaned_number = "".join(filter(str.isdigit, number_part))

    if not cleaned_number:
        return "None"

    type_part_norm = type_part_raw.lower().strip().replace("ё", "е")
    is_account = (
        ("счет" in type_part_norm)
        or ("счёт" in type_part_norm)
        or (len(cleaned_number) == 20)
    )

    if is_account:
        if len(cleaned_number) < 4:
            return "None"
        return "Счет **" + cleaned_number[-4:]

    if len(cleaned_number) == 16:
        masked = (
            f"{cleaned_number[:4]} {cleaned_number[4:6]}** **** {cleaned_number[-4:]}"
        )
        if type_part_raw:
            return f"{type_part_raw} {masked}"
        return masked

    if len(cleaned_number) >= 4:
        return "Счет **" + cleaned_number[-4:]

    return "None"


def get_date(date_str: str) -> str:
    if not isinstance(date_str, str) or not date_str.strip():
        return ""

    s = date_str.strip()
    try:
        dt_obj = datetime.fromisoformat(s)
        return dt_obj.strftime("%d.%m.%Y")
    except Exception:
        pass

    for fmt in ("%d.%m.%Y", "%Y-%m-%d", "%d-%m-%Y", "%Y.%m.%d"):
        try:
            dt_obj = datetime.strptime(s, fmt)
            return dt_obj.strftime("%d.%m.%Y")
        except Exception:
            continue

    return s


def read_excel_file(file_path: Path) -> List[Dict[str, Any]]:
    df = pd.read_excel(file_path)
    records = df.to_dict(orient="records")
    return [{str(k): v for k, v in record.items()} for record in records]


def normalize_transaction(tx: Dict[str, Any]) -> Dict[str, Any]:
    if not isinstance(tx, dict) or not tx:
        return {}

    op = tx.get("operationAmount")
    if isinstance(op, dict):
        amt = _to_float(op.get("amount"))
        if amt is not None:
            op["amount"] = amt
            tx["operationAmount"] = op
        return tx

    if op is not None and op != "":
        amt = _to_float(op)
        tx["operationAmount"] = amt if amt is not None else None
        return tx

    if "operationAmount" not in tx and "amount" in tx:
        amt = _to_float(tx.get("amount"))
        if amt is None:
            tx["operationAmount"] = None
            return tx

        code = str(tx.get("currency_code", "")).strip()
        name = str(tx.get("currency_name", "")).strip()
        tx["operationAmount"] = {
            "amount": amt,
            "currency": {"name": name, "code": code},
        }
        return tx

    return tx


def normalize_transactions(transactions: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    result: List[Dict[str, Any]] = []
    for tx in transactions:
        ntx = normalize_transaction(tx)
        if ntx:
            result.append(ntx)
    return result


def process_transaction_safe(tx: Dict[str, Any]) -> Optional[float]:
    op = tx.get("operationAmount")

    if isinstance(op, dict):
        return _to_float(op.get("amount"))
    return _to_float(op)


def filter_by_description_keyword(
    transactions: List[Dict[str, Any]], keyword: str
) -> List[Dict[str, Any]]:
    kw = (keyword or "").strip().lower()
    if not kw:
        return transactions

    result: List[Dict[str, Any]] = []
    for tx in transactions:
        desc = str(tx.get("description", "")).lower()
        if kw in desc:
            result.append(tx)
    return result


def ask_sort_reverse() -> bool:
    while True:
        choice = (
            input(
                "\nПрограмма: Выберите порядок сортировки:\n"
                "1 - по возрастанию (сначала старые)\n"
                "2 - по убыванию (сначала новые)\n"
                "Пользователь: "
            )
            .strip()
            .lower()
        )

        if choice in ("1", "по возрастанию", "возрастанию", "asc", "a"):
            return False
        if choice in ("2", "по убыванию", "убыванию", "desc", "d"):
            return True
        print("\nПрограмма: Некорректный выбор. Введите 1 или 2.")


def main() -> None:
    try:
        print(
            "\nПрограмма: Привет! Добро пожаловать в программу работы с банковскими транзакциями."
        )
        print("Выберите необходимый пункт меню:")
        print("1. Получить информацию о транзакциях из JSON-файла")
        print("2. Получить информацию о транзакциях из CSV-файла")
        print("3. Получить информацию о транзакциях из XLSX-файла")

        choice = input("\nПользователь: ").strip()
        transactions: List[Dict[str, Any]] = []

        if choice == "1":
            file_path = Path(
                r"C:\Users\Пользователь\PycharmProjects\PythonProject\data\operations.json"
            )
            if not file_path.exists():
                print(f"\nПрограмма: Файл не найден: {file_path}")
                return
            transactions = load_transactions(str(file_path))
            print("\nПрограмма: Для обработки выбран JSON-файл.")

        elif choice == "2":
            file_path = Path(
                r"C:\Users\Пользователь\PycharmProjects\PythonProject\data\transactions.csv"
            )
            if not file_path.exists():
                print(f"\nПрограмма: Файл не найден: {file_path}")
                return
            transactions = read_csv_file(str(file_path))
            print("\nПрограмма: Для обработки выбран CSV-файл.")

        elif choice == "3":
            file_path = Path(
                r"C:\Users\Пользователь\PycharmProjects\PythonProject\data\transactions_excel.xlsx"
            )
            if not file_path.exists():
                print(f"\nПрограмма: Файл не найден: {file_path}")
                return
            transactions = read_excel_file(file_path)
            print("\nПрограмма: Для обработки выбран XLSX-файл.")
        else:
            print("\nПрограмма: Неверный выбор формата файла")
            return

        if not transactions:
            print("\nПрограмма: Ошибка загрузки данных или файл пуст")
            return

        transactions = normalize_transactions(transactions)

        valid_states = {"EXECUTED", "CANCELED", "PENDING"}
        state = ""
        while state not in valid_states:
            state = (
                input(
                    "\nПрограмма: Введите статус, по которому необходимо выполнить фильтрацию.\n"
                    "Доступные для фильтровки статусы: EXECUTED, CANCELED, PENDING\n"
                    "Пользователь: "
                )
                .strip()
                .upper()
            )
            if state not in valid_states:
                print(f"\nПрограмма: Статус операции {state} недоступен.")

        filtered_transactions = filter_by_state(transactions, state)
        print(f'\nПрограмма: Операции отфильтрованы по статусу "{state}"')

        sort_choice = (
            input("\nПрограмма: Отсортировать операции по дате? Да/Нет\nПользователь: ")
            .strip()
            .lower()
        )
        if sort_choice in ("да", "yes"):
            reverse = ask_sort_reverse()
            filtered_transactions = sort_by_date(filtered_transactions, reverse=reverse)

        rub_choice = (
            input(
                "\nПрограмма: Выводить только рублевые транзакции? Да/Нет\nПользователь: "
            )
            .strip()
            .lower()
        )
        if rub_choice in ("да", "yes"):
            filtered_transactions = [
                tx
                for tx in filtered_transactions
                if (
                    isinstance(tx.get("operationAmount"), dict)
                    and str(
                        tx.get("operationAmount", {})
                        .get("currency", {})
                        .get("code", "")
                    ).upper()
                    == "RUB"
                )
                or (isinstance(tx.get("operationAmount"), (int, float)))
            ]

        search_choice = (
            input(
                "\nПрограмма: Отфильтровать список транзакций по определенному слову в описании? Да/Нет\n"
                "Пользователь: "
            )
            .strip()
            .lower()
        )
        if search_choice in ("да", "yes"):
            keyword = input(
                "\nПрограмма: Введите слово для поиска в описании\nПользователь: "
            ).strip()
            filtered_transactions = filter_by_description_keyword(
                filtered_transactions, keyword
            )

        print("\nПрограмма: Распечатываю итоговый список транзакций...")
        if not filtered_transactions:
            print(
                "\nПрограмма: Не найдено ни одной транзакции, подходящей под ваши условия фильтрации."
            )
            return

        print(
            f"\nПрограмма: Всего банковских операций в выборке: {len(filtered_transactions)}"
        )
        for tx in filtered_transactions:
            try:
                date_str = tx.get("date", "")
                if not date_str:
                    continue
                date = get_date(date_str)
                description = tx.get("description", "Не указано")
                from_masked = mask_account_card(tx.get("from", ""))
                to_masked = mask_account_card(tx.get("to", ""))
                op = tx.get("operationAmount")
                amount = process_transaction_safe(tx)

                print(f"\n{date} {description}")
                if from_masked != "None" and to_masked != "None":
                    print(f"{from_masked} -> {to_masked}")
                elif from_masked != "None":
                    print(from_masked)
                elif to_masked != "None":
                    print(to_masked)

                if op is None or op == "" or amount is None:
                    print("Сумма: данные отсутствуют")
                    continue

                if isinstance(op, dict):
                    cur = op.get("currency") or {}
                    code = str(cur.get("code", "")).strip()
                    name = str(cur.get("name", "")).strip()
                    cur_text = currency_label(code, name)
                else:
                    cur_text = "руб."

                print(f"Сумма: {format_amount(amount)} {cur_text}")

            except Exception as e:
                print(f"\nОшибка при обработке транзакции: {str(e)}")

    except KeyboardInterrupt:
        print("\nПрограмма: Работа прервана пользователем.")
    except Exception as e:
        print(f"\nПрограмма: Произошла ошибка: {str(e)}")
    finally:
        print("\nПрограмма: Работа завершена.")


if __name__ == "__main__":
    main()

from io import StringIO
from unittest.mock import patch

from src import main as m

import unittest
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from src.utils import load_transactions
from src.financial_operations_reader import read_csv_file
from src.processing import sort_by_date, filter_by_state



class TestMoreHelpers(unittest.TestCase):
    def test__to_float_none(self):
        self.assertIsNone(m._to_float(None))

    def test__to_float_empty_string(self):
        self.assertIsNone(m._to_float("   "))

    def test__to_float_comma_and_spaces(self):
        self.assertEqual(m._to_float("1 234,50"), 1234.5)

    def test__to_float_invalid(self):
        self.assertIsNone(m._to_float("abc"))

    def test_get_date_simple_yyyy_mm_dd(self):
        self.assertEqual(m.get_date("2023-10-05"), "05.10.2023")

    def test_get_date_unknown_format_returns_original(self):
        self.assertEqual(m.get_date("05/10/2023"), "05/10/2023")

    def test_mask_account_card_schet_with_yo(self):
        self.assertEqual(m.mask_account_card("Счёт 1234567890"), "Счет **7890")

    def test_mask_account_card_20_digits_without_word(self):
        self.assertEqual(
            m.mask_account_card("12345678901234567890"),
            "Счет **7890"
        )

    def test_mask_account_card_too_short_digits(self):
        self.assertEqual(m.mask_account_card("Счет 123"), "None")



class TestNormalizeTransaction(unittest.TestCase):
    def test_normalize_transaction_operationAmount_dict_amount_str_to_float(self):
        tx = {
            "operationAmount": {
                "amount": "1000.50",
                "currency": {"code": "USD", "name": "USD"}
            }
        }
        out = m.normalize_transaction(tx)
        self.assertIsInstance(out["operationAmount"]["amount"], float)
        self.assertEqual(out["operationAmount"]["amount"], 1000.5)

    def test_normalize_transaction_operationAmount_str_to_float(self):
        tx = {"operationAmount": "2000"}
        out = m.normalize_transaction(tx)
        self.assertEqual(out["operationAmount"], 2000.0)

    def test_normalize_transaction_csv_shape_builds_operationAmount(self):
        tx = {
            "amount": "130",
            "currency_code": "USD",
            "currency_name": "USD",
            "description": "Перевод"
        }
        out = m.normalize_transaction(tx)
        self.assertIsInstance(out["operationAmount"], dict)
        self.assertEqual(out["operationAmount"]["amount"], 130.0)
        self.assertEqual(out["operationAmount"]["currency"]["code"], "USD")
        self.assertEqual(out["operationAmount"]["currency"]["name"], "USD")

    def test_normalize_transactions_drops_empty_dicts(self):
        txs = [
            {},
            {"amount": "10", "currency_code": "RUB", "currency_name": "руб."}
        ]
        out = m.normalize_transactions(txs)
        self.assertEqual(len(out), 1)



class TestSearchAndSortHelpers(unittest.TestCase):
    def test_filter_by_description_keyword_empty_keyword_returns_same(self):
        txs = [{"description": "Перевод"}, {"description": "Открытие вклада"}]
        out = m.filter_by_description_keyword(txs, "")
        self.assertEqual(out, txs)

    def test_filter_by_description_keyword_finds_case_insensitive(self):
        txs = [
            {"description": "Перевод организации"},
            {"description": "Открытие вклада"}
        ]
        out = m.filter_by_description_keyword(txs, "ОРГАНИЗАЦИИ")
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["description"], "Перевод организации")

    @patch("builtins.input", side_effect=["что-то", "1"])
    def test_ask_sort_reverse_loops_until_valid(self, mock_input):
        rev = m.ask_sort_reverse()
        self.assertFalse(rev)

    @patch("builtins.input", side_effect=["x", "2"])
    def test_ask_sort_reverse_choose_desc(self, mock_input):
        rev = m.ask_sort_reverse()
        self.assertTrue(rev)



class TestMainMoreBranches(unittest.TestCase):
    @patch("pathlib.Path.exists", return_value=True)
    @patch("src.main.sort_by_date")
    @patch("src.main.filter_by_state")
    @patch("src.main.load_transactions")
    @patch("builtins.input")
    def test_main_rub_filter_keeps_only_rub(
        self,
        mock_input,
        mock_load_transactions,
        mock_filter_by_state,
        mock_sort_by_date,
        mock_exists,
    ):
        txs = [
            {
                "id": 1,
                "date": "2019-12-08T22:46:21.935582",
                "description": "Открытие вклада",
                "to": "Счет 12345678901234564321",
                "operationAmount": {
                    "amount": "40542",
                    "currency": {"code": "RUB", "name": "руб."}
                },
                "state": "EXECUTED",
            },
            {
                "id": 2,
                "date": "2019-12-07T22:46:21.935582",
                "description": "Открытие вклада",
                "to": "Счет 12345678901234560034",
                "operationAmount": {
                    "amount": "10",
                    "currency": {"code": "USD", "name": "USD"}
                },
                "state": "EXECUTED",
            },
        ]

        mock_load_transactions.return_value = txs
        mock_filter_by_state.return_value = txs
        mock_sort_by_date.return_value = txs
        mock_input.side_effect = [
            "1",          # JSON
            "EXECUTED",   # статус
            "нет",        # сортировать
            "да",         # только рублёвые
            "нет",        # фильтр по слову
        ]
        with patch("sys.stdout", new_callable=StringIO) as fake_out:
            m.main()
            output = fake_out.getvalue()
        self.assertIn("Всего банковских операций в выборке: 1", output)
        self.assertIn("Сумма: 40542 руб.", output)
        self.assertNotIn("USD", output)

    @patch("pathlib.Path.exists", return_value=True)
    @patch("src.main.sort_by_date")
    @patch("src.main.filter_by_state")
    @patch("src.main.load_transactions")
    @patch("builtins.input")
    def test_main_search_filter_reduces_list(
        self,
        mock_input,
        mock_load_transactions,
        mock_filter_by_state,
        mock_sort_by_date,
        mock_exists,
    ):
        txs = [
            {
                "id": 1,
                "date": "2019-11-12T10:00:00",
                "description": "Перевод с карты на карту",
                "from": "MasterCard 7771271234",
                "from": "MasterCard 7771271234563727",
                "to": "Visa Platinum 1293381234569203",
                "operationAmount": {
                    "amount": "130",
                    "currency": {"code": "USD", "name": "USD"}
                },
                "state": "CANCELED",
            },
            {
                "id": 2,
                "date": "2019-11-12T11:00:00",
                "description": "Открытие вклада",
                "to": "Счет 12345678901234564321",
                "operationAmount": {
                    "amount": "1",
                    "currency": {"code": "RUB", "name": "руб."}
                },
                "state": "CANCELED",
            },
        ]
        mock_load_transactions.return_value = txs
        mock_filter_by_state.return_value = txs
        mock_sort_by_date.return_value = txs
        mock_input.side_effect = [
            "1",          # JSON
            "CANCELED",   # статус
            "нет",        # сортировать
            "нет",        # только рублёвые
            "да",         # фильтр по слову
            "карты",      # ключевое слово
        ]
        with patch("sys.stdout", new_callable=StringIO) as fake_out:
            m.main()
            output = fake_out.getvalue()
        self.assertIn("Всего банковских операций в выборке: 1", output)
        self.assertIn("Перевод с карты на карту", output)
        self.assertNotIn("Открытие вклада", output)



class TestLoadTransactionsJson(unittest.TestCase):
    def test_load_json_transactions(self):
        tmp = NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8")
        try:
            json.dump([{"id": 1, "amount": 100}], tmp, ensure_ascii=False)
            tmp.close()

            txs = load_transactions(Path(tmp.name))
            self.assertEqual(len(txs), 1)
            self.assertEqual(txs[0]["id"], 1)
            self.assertEqual(txs[0]["amount"], 100)
        finally:
            os.unlink(tmp.name)

    def test_load_nonexistent_file_raises_or_empty(self):
        p = Path("definitely_not_exists_12345.json")
        try:
            txs = load_transactions(p)
        except FileNotFoundError:
            return
        self.assertEqual(txs, [])



class TestReadCsvFile(unittest.TestCase):
    def test_read_csv_file_reads_semicolon_csv(self):
        tmp = NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8")
        try:
            tmp.write("id;state;date;amount;currency_name;currency_code;from;to;description\n")
            tmp.write("1;CANCELED;2019-11-12T10:00:00;130;USD;USD;MasterCard 7771271234563727;Visa Platinum 1293381234569203;Перевод с карты на карту\n")
            tmp.close()

            txs = read_csv_file(tmp.name)
            self.assertEqual(len(txs), 1)
            self.assertEqual(txs[0]["id"], 1)
            self.assertEqual(txs[0]["currency_code"], "USD")
            self.assertEqual(txs[0]["amount"], 130)
        finally:
            os.unlink(tmp.name)



class TestSortByDate(unittest.TestCase):
    def test_sort_by_date_ascending(self):
        txs = [
            {"date": "2023-01-01T12:00:00"},
            {"date": "2022-01-01T12:00:00"},
            {"date": "2024-01-01T12:00:00"}
        ]
        sorted_txs = m.sort_by_date(txs, reverse=False)
        self.assertEqual(sorted_txs[0]["date"], "2022-01-01T12:00:00")
        self.assertEqual(sorted_txs[1]["date"], "2023-01-01T12:00:00")
        self.assertEqual(sorted_txs[2]["date"], "2024-01-01T12:00:00")

    def test_sort_by_date_descending(self):
        txs = [
            {"date": "2023-01-01T12:00:00"},
            {"date": "2022-01-01T12:00:00"},
            {"date": "2024-01-01T12:00:00"}
        ]
        sorted_txs = m.sort_by_date(txs, reverse=True)
        self.assertEqual(sorted_txs[0]["date"], "2024-01-01T12:00:00")
        self.assertEqual(sorted_txs[1]["date"], "2023-01-01T12:00:00")
        self.assertEqual(sorted_txs[2]["date"], "2022-01-01T12:00:00")



class TestFilterByState(unittest.TestCase):
    def test_filter_by_state_executed(self):
        txs = [
            {"state": "EXECUTED"},
            {"state": "CANCELED"},
            {"state": "EXECUTED"}
        ]
        filtered = filter_by_state(txs, "EXECUTED")
        self.assertEqual(len(filtered), 2)
        self.assertTrue(all(tx["state"] == "EXECUTED" for tx in filtered))

    def test_filter_by_state_unknown_returns_empty_or_original(self):
        txs = [{"state": "EXECUTED"}, {"state": "CANCELED"}]
        filtered = filter_by_state(txs, "UNKNOWN_STATE")
        self.assertTrue(filtered == [] or filtered == txs)


if __name__ == "__main__":
    unittest.main()
