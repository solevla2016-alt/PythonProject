import pytest
from datetime import datetime
# Подставьте корректный путь к вашим функциям
from src.processing import filter_by_state, sort_by_date
from src.mask import get_mask_card_number, get_mask_account  # скорректируйте путь



# --- Тесты для filter_by_state ---

@pytest.mark.parametrize(
    "input_data, state, expected_result",
    [
        (
            [{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "PENDING"}],
            "EXECUTED",
            [{"id": 1, "state": "EXECUTED"}],
        ),
        (
            [{"id": 1, "state": "CANCELED"}, {"id": 2, "state": "EXECUTED"}],
            "CANCELED",
            [{"id": 1, "state": "CANCELED"}],
        ),
        ([], "EXECUTED", []),
    ],
)
def test_filter_by_state(input_data, state, expected_result):
    result = filter_by_state(input_data, state)
    assert result == expected_result



# --- Тесты для sort_by_date ---

@pytest.mark.parametrize(
    "transactions, reverse, expected_order",
    [
        (
            [
                {
                    "id": 1,"state": "EXECUTED", "date": "2019-07-03T18:35:29.512364",},
                {
                    "id": 2,"state": "EXECUTED","date": "2018-06-30T02:08:58.425572",},
            ],
            True,
            ["2019-07-03", "2018-06-30"],
        ),
        (
            [
                {
                    "id": 1,"state": "EXECUTED","date": "2019-07-03T18:35:29.512364",},
                {
                    "id": 2,"state": "EXECUTED","date": "2018-06-30T02:08:58.425572",},
            ],
            False,
            ["2018-06-30", "2019-07-03"],
        ),
        ([], True, []),
    ],
)
def test_sort_by_date(transactions, reverse, expected_order):
    sorted_transactions = sort_by_date(transactions, reverse)
    actual_dates = [
        datetime.strptime(t["date"].split("T")[0], "%Y-%m-%d").strftime("%Y-%m-%d")
        for t in sorted_transactions
    ]
    assert actual_dates == expected_order



# --- Тесты для get_mask_card_number ---

@pytest.mark.parametrize(
    "card_number, expected",
    [
        # Валидные номера карт (16 цифр)
        ("1234567890123456", "1234 56** **** 3456"),
        ("0000111122223333", "0000 11** **** 3333"),
        ("9999888877776666", "9999 88** **** 6666"),
        # Невалидные случаи
        ("", ""),  # пустая строка
        ("123", ""),  # меньше 16 цифр
        ("12345678901234567", ""),  # больше 16 цифр
        ("1234abcd56789012", ""),  # нецифровые символы
        ("1234 5678 9012 3456", ""),  # пробелы
        ("1234-5678-9012-3456", ""),  # дефисы
        ("1234_5678_9012_3456", ""),  # подчёркивания
        (" 1234567890123456 ", ""),  # пробелы по краям
    ],
)
def test_get_mask_card_number(card_number, expected):
    result = get_mask_card_number(card_number)
    assert result == expected



# --- Тесты для get_mask_account ---

@pytest.mark.parametrize(
    "account_number, expected",
    [
        # Валидные номера счетов (≥4 цифр)
        ("12345678", "**5678"),  # было "**78"
        ("0000", "**0000"),
        ("999999", "**9999"),
        ("1234", "**1234"),       # было "**34"
        ("1111111111", "**1111"),  # было "**11"
        # Невалидные случаи (остаются без изменений)
        ("", ""),
        ("12", ""),
        ("12a4", ""),
        ("1 234", ""),
        ("abcd", ""),
        ("12#4", ""),
        ("  1234  ", ""),
    ],
)
def test_get_mask_account(account_number, expected):
    result = get_mask_account(account_number)
    assert result == expected