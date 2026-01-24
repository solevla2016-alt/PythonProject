import pytest
from src.mask import get_mask_card_number
from src.mask import get_mask_account
import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


def test_get_mask_card_number_valid():
    assert get_mask_card_number("1234567890123456") == "1234 56** **** 3456"

def test_get_mask_card_number_invalid_length():
    assert get_mask_card_number("1234") == ""

def test_get_mask_card_number_non_digit():
    assert get_mask_card_number("abcd567890123456") == ""

def test_get_mask_account_valid():
    assert get_mask_account("1234567890") == "**7890"

def test_get_mask_account_invalid_length():
    assert get_mask_account("123") == ""

def test_get_mask_account_non_digit():
    assert get_mask_account("abcd") == ""