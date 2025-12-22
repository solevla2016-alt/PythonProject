import pytest
from src.mask import get_mask_card_number

@pytest.mark.parametrize('card_number, expected', [
    ('1234567890123456', '1234 56** **** 3456'),
    ('123456789012345', ""),
    ('abcde', ""),
])
def test_get_mask_card_number(card_number, expected):
    assert get_mask_card_number(card_number) == expected


from src.mask import get_mask_account

@pytest.mark.parametrize('account_number, expected', [
        ('1234567890123456', '**3456'),
        ('1234', '**34'),
        ('123', ""),
        ('abcdef', ""),
    ])
def test_get_mask_account(account_number, expected):
        assert get_mask_account(account_number) == expected

