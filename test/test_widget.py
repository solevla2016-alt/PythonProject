import pytest
from src.widget import mask_account_card
from src.widget import get_date

@pytest.mark.parametrize('info_str, expected', [
    ("Visa Platinum 7000792289606361", "7000 79** **** 6361"),
    ("MasterCard Gold 1234567890123456", "1234 56** **** 3456"),
    ("Счет 40817810800000000001", "**0001"),
    ("Invalid Input", "None"),
])
def test_mask_account_card(info_str, expected):
    assert mask_account_card(info_str) == expected




@pytest.mark.parametrize('date_str, expected', [
    ("2024-03-11T02:26:18.671407", "11.03.2024"),
    ("2023-12-31T23:59:59.999999", "31.12.2023"),
    ("invalid-date-format", ValueError),  # Ожидаемая ошибка при неверном формате
])
def test_get_date(date_str, expected):
    try:
        result = get_date(date_str)
        assert result == expected
    except Exception as e:
        assert isinstance(e, expected)