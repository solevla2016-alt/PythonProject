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