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

import functools
from datetime import datetime
from typing import Callable, Any, Optional


def log(filename: Optional[str] = None) -> Callable:
    """Декоратор для логирования начала и конца выполнения функции, а также результатов или возникающих ошибок.

    Аргументы:
        filename (str, optional): Имя файла, в который будут записаны логи. По умолчанию None,
        что означает вывод в консоль.

           Возможные сценарии использования:
        - Простое ведение журнала всех вызовов функций.
        - Анализ поведения программы и диагностика ошибок.
    """

    def decorator(func: Callable) -> Callable:
        """Обертка над оригинальной функцией."""

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Основная логика выполнения декорированной функции с обработкой логов."""
            try:
                # Выполняем оригинальную функцию и получаем результат
                result = func(*args, **kwargs)

                # Создаем сообщение о результате
                message = f"{func.__name__}: {result}"

                # Записываем лог в файл или выводим в консоль
                if filename:
                    with open(filename, mode="a", encoding="utf-8") as file:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        file.write(f"[{timestamp}] {message}\n")
                else:
                    print(message)

                return result

            except Exception as e:
                # Сообщение об ошибке с указанием имени функции, типа ошибки и входных параметров
                err_message = f"{func.__name__}: error: {type(e).__name__}. Inputs: {args}, {kwargs}"

                # Записываем ошибку в файл или выводим в консоль
                if filename:
                    with open(filename, mode="a", encoding="utf-8") as file:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        file.write(f"[{timestamp}] {err_message}\n")
                else:
                    print(err_message)

        return wrapper

    return decorator

import unittest
import os
from io import StringIO
from contextlib import redirect_stdout
from datetime import datetime


from src.decorators import log

class TestLogDecorator(unittest.TestCase):
    def setUp(self):
        self.test_file_name = "test_log.txt"
        if os.path.exists(self.test_file_name):
            os.remove(self.test_file_name)

    def tearDown(self):
        if os.path.exists(self.test_file_name):
            os.remove(self.test_file_name)

    def test_successful_execution_console_output(self):
        """Тестируем успешное выполнение функции с выводом в консоль"""
        output = StringIO()  # Перенаправляем stdout для захвата вывода

        @log()
        def successful_func():
            return "OK"

        with redirect_stdout(output):
            successful_func()

        # Проверяем содержимое консоли
        captured_output = output.getvalue().strip()
        expected_result = f'successful_func: OK'
        self.assertIn(expected_result, captured_output)

    def test_error_handling_console_output(self):
        """Тестируем возникновение ошибки с выводом в консоль"""
        output = StringIO()  # Перенаправляем stdout для захвата вывода

        @log()
        def failing_func():
            raise ValueError("Test Error")

        with redirect_stdout(output):
            try:
                failing_func()
            except ValueError:
                pass

        # Проверяем содержимое консоли
        captured_output = output.getvalue().strip()
        expected_result = f'failing_func: error: ValueError. Inputs: (), {{}}'
        self.assertIn(expected_result, captured_output)

    def test_successful_execution_file_logging(self):
        """Тестируем успешное выполнение функции с логированием в файл"""
        @log(filename=self.test_file_name)
        def successful_func():
            return "OK"

        successful_func()

        # Читаем содержимое файла
        with open(self.test_file_name, 'r', encoding='utf-8') as file:
            content = file.read().strip()

        expected_result = f'successful_func: OK'
        self.assertIn(expected_result, content)

    def test_error_handling_file_logging(self):
        """Тестируем возникновение ошибки с логированием в файл"""
        @log(filename=self.test_file_name)
        def failing_func():
            raise TypeError("Test Error")

        try:
            failing_func()
        except TypeError:
            pass

        # Читаем содержимое файла
        with open(self.test_file_name, 'r', encoding='utf-8') as file:
            content = file.read().strip()

        expected_result = f'failing_func: error: TypeError. Inputs: (), {{}}'
        self.assertIn(expected_result, content)

if __name__ == '__main__':
    unittest.main()
