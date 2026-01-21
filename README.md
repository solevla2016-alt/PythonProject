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


import json
import os
from typing import Any, Dict, List


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Функция загружает список словарей с информацией о финансовых операциях из JSON-файла.

    """
    try:
        # Проверяем наличие файла
        if not os.path.exists(file_path):
            return []

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            return data
        else:
            return []
    except Exception as e:
        print(f"Ошибка загрузки данных: {e}")
        return []

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

import os
import requests
from typing import Dict, Union
from dotenv import load_dotenv

# 1. Загружаем .env из корневой директории
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)

# 2. Отладка: проверяем загрузку ключа
print("→ Проверка окружения:")
api_key = os.getenv("API_KEY")
if api_key:
    print(f"  API_KEY загружен (длина: {len(api_key)})")
    print(f"  Пример: {api_key[:4]}...{api_key[-4:]}")
else:
    print("  ERROR: API_KEY не найден в .env!")

print("-" * 40)


def convert_to_rubles(amount: float, currency: str) -> float:
    """Конвертирует сумму из валюты в RUB через APILayer."""
    api_key = os.getenv("API_KEY")

    if not api_key:
        raise ValueError("API_KEY не найден в .env. Убедитесь, что файл .env существует и содержит API_KEY.")

    url = "https://api.apilayer.com/exchangerates_data/convert"


    params: Dict[str, str] = {
        "from": str(currency),
        "to": "RUB",
        "amount": str(float(amount))
    }
    headers: Dict[str, str] = {"apikey": api_key}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()

        if not data.get("success"):
            err_info = data.get("error", {}).get("info", "Неизвестная ошибка")
            raise Exception(f"API ошибка: {err_info}")

        converted_amount = float(data["result"])
        return round(converted_amount, 2)

    except requests.exceptions.RequestException as e:
        raise Exception(f"Сеть/запрос ошибка: {e}")


def process_transaction(transaction: Dict[str, Union[float, str]]) -> float:
    """Обрабатывает транзакцию и возвращает сумму в рублях."""

    amount_value = transaction["amount"]
    if isinstance(amount_value, (int, float)):
        amount = float(amount_value)
    elif isinstance(amount_value, str):
        try:
            amount = float(amount_value)
        except ValueError:
            raise ValueError(f"amount должен быть числом, получено: {amount_value}")
    else:
        raise TypeError(f"amount должен быть числом или строкой, получено: {type(amount_value)}")


    currency_value = transaction["currency"]
    if not isinstance(currency_value, str):
        raise TypeError(
            f"currency должно быть строкой, получено: {type(currency_value)}"
        )
    currency = currency_value.upper().strip()

    if currency == "RUB":
        return amount

    if currency not in ("USD", "EUR"):
        raise ValueError(
            f"Валюта {currency} не поддерживается. Используйте USD, EUR, RUB."
        )

    return convert_to_rubles(amount, currency)


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


Скопируйте .env.example в .env:

bash
cp .env.example .env
Заполните .env своими реальными ключами и настройками.
