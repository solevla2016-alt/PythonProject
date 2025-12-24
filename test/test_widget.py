import pytest

from src.widget import get_date, mask_account_card


@pytest.mark.parametrize(
    "info_str, expected",
    [
        ("Visa Platinum 7000792289606361", "7000 79** **** 6361"),
        ("MasterCard Gold 1234567890123456", "1234 56** **** 3456"),
        ("Счет 40817810800000000001", "**0001"),
        ("Invalid Input", "None"),
    ],
)
def test_mask_account_card(info_str, expected):
    assert mask_account_card(info_str) == expected


def test_get_date_valid(valid_date_formats):
    """Проверяет корректное преобразование валидных форматов даты."""
    for date_str, expected in valid_date_formats:
        result = get_date(date_str)
        assert result == expected, f"Ошибка для {date_str}: получено {result}, ожидалось {expected}"
