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
