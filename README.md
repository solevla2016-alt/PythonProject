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
Тестовые сценарии (pytest)
Тесты для src/masks.py
Файл: tests/test_masks.py

python
import pytest
from src.masks import get_mask_card_number, get_mask_account



@pytest.mark.parametrize("card_number, expected", [
    ("1234567890123456", "1234 56** **** 3456"),
    ("123456789012345", None),   # <16 цифр
    ("abcde", None),            # не цифры
    ("", None),                 # пустая строка
    ("1234a67890123456", None), # есть буквы
])
def test_get_mask_card_number(card_number, expected):
    assert get_mask_card_number(card_number) == expected




@pytest.mark.parametrize("account_number, expected", [
    ("1234567890123456", "**3456"),
    ("1234", "**34"),
    ("123", None),              # <4 цифр
    ("abcdef", None),           # не цифры
    ("", None),                # пустая строка
])
def test_get_mask_account(account_number, expected):
    assert get_mask_account(account_number) == expected
Тесты для src/widget.py
Файл: tests/test_widget.py

python
import pytest
from src.widget import mask_account_card, get_date



@pytest.mark.parametrize("info_str, expected", [
    ("Visa Platinum 7000792289606361", "7000 79** **** 6361"),
    ("MasterCard Gold 1234567890123456", "1234 56** **** 3456"),
    ("Счет 40817810800000000001", "**0001"),
    ("Debit Card 1234567890123456", "1234 56** **** 3456"),
    ("Invalid Input", "None"),
    ("", "None"),  # пустая строка
])
def test_mask_account_card(info_str, expected):
    assert mask_account_card(info_str) == expected




@pytest.mark.parametrize("date_str, expected", [
    ("2024-03-11T02:26:18.671407", "11.03.2024"),
    ("2023-12-31T23:59:59.999999", "31.12.2023"),
])
def test_get_date_valid(date_str, expected):
    assert get_date(date_str) == expected



def test_get_date_invalid():
    with pytest.raises(ValueError):
        get_date("invalid-date-format")
Тесты для src/processing.py
Файл: tests/test_processing.py

python
import pytest
from src.processing import filter_by_state, sort_by_date

# Общие данные для тестов
data = [
    {"id": 41428829, "state": "

rom typing import Dict, List, Iterator, Any

def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> Iterator[Dict[str, Any]]:
    """
    Возвращает итератор, выдающий транзакции с указанной валютой.
    """
    for transaction in transactions:
        if (
            transaction.get("operationAmount", {})
              .get("currency", {})
              .get("code") == currency_code
        ):
            yield transaction


if __name__ == "__main__":

    transactions = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
    ]

    usd_transactions = filter_by_currency(transactions, "USD")
    for _ in range(2):
        print(next(usd_transactions))


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """
    Генерирует последовательность описаний транзакций.
    """
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генератор, выдающий номера банковских карт в формате XXXX XXXX XXXX XXXX.
    """
    for number in range(start, end + 1):
        formatted_card = f"{number:016d}"
        yield " ".join([formatted_card[i:i+4] for i in range(0, 16, 4)])


import pytest
from src.generators import filter_by_currency
from src.generators import transaction_descriptions
from src.generators import card_number_generator


def test_filter_by_currency_with_valid_currency(currency_transactions):
    """Проверка фильтрации по существующей валюте."""
    filtered = list(filter_by_currency(currency_transactions, "USD"))  # Исправлено: currency_transactions
    assert len(filtered) == 2
    assert all(tx["operationAmount"]["currency"]["code"] == "USD" for tx in filtered)

def test_filter_by_currency_no_matches(currency_transactions):
    """Проверка случая, когда заданная валюта отсутствует."""
    filtered = list(filter_by_currency(currency_transactions, "GBP"))
    assert len(filtered) == 0

def test_filter_by_currency_empty_list():
    """Проверка функционирования с пустым списком транзакций."""
    filtered = list(filter_by_currency([], "USD"))
    assert len(filtered) == 0


def test_transaction_descriptions_valid_input(description_transactions):
    """Проверка верного возврата описаний транзакций."""
    descriptions = list(transaction_descriptions(description_transactions))
    assert descriptions == ["Оплата услуг", "Пополнение счёта", "Покупка товаров"]

def test_transaction_descriptions_empty_list():
    """Проверка работы с пустым списком транзакций."""
    descriptions = list(transaction_descriptions([]))
    assert len(descriptions) == 0


@pytest.mark.parametrize("start,end,expected", [
    (1, 3, ["0000 0000 0000 0001", "0000 0000 0000 0002", "0000 0000 0000 0003"]),
    (9999, 10001, ["0000 0000 0000 9999", "0000 0000 0001 0000", "0000 0000 0001 0001"])
])
def test_card_number_generator_valid_range(start, end, expected):
    numbers = list(card_number_generator(start, end))
    assert numbers == expected

def test_card_number_generator_edge_cases():
    """Проверка краевых случаев диапазонов."""
    edge_cases = list(card_number_generator(1, 1))  # Один элемент
    assert edge_cases == ["0000 0000 0000 0001"]

    empty_case = list(card_number_generator(1, 0))  # Неверный порядок границ
    assert len(empty_case) == 0
