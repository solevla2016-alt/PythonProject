import pytest

from src.mask import get_mask_account, get_mask_card_number


@pytest.mark.parametrize(
    "card_number, expected",
    [
        ("1234567890123456", "1234 56** **** 3456"),
        ("123456789012345", ""),
        ("abcde", ""),
    ],
)
def test_get_mask_card_number(card_number, expected):
    assert get_mask_card_number(card_number) == expected


@pytest.mark.parametrize(
    "account_number, expected",
    [
        ("1234567890123456", "**3456"),
        ("123", ""),
        ("abcdef", ""),
    ],
)
def test_get_mask_account(account_number, expected):
    assert get_mask_account(account_number) == expected
