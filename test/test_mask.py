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

