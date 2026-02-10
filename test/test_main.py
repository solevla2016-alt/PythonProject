import logging
from unittest.mock import patch

import pytest

import src.main as m

logging.disable(logging.CRITICAL)



def test_to_float_none():
    assert m.to_float(None) is None

def test_to_float_int():
    assert m.to_float(10) == 10.0

def test_to_float_spaces_and_comma():
    assert m.to_float("1 234,50") == 1234.5

def test_to_float_invalid():
    assert m.to_float("abc") is None

def test_format_amount_integer():
    assert m.format_amount(130.0) == "130"

def test_format_amount_float_trim_zeros():
    assert m.format_amount(1000.50) == "1000.5"

def test_format_currency_rub():
    assert m.format_currency("RUB", "Российский рубль") == "руб."

def test_format_currency_usd():
    assert m.format_currency("USD", "USD") == "USD"

def test_format_currency_fallback_to_name():
    assert m.format_currency("", "EUR") == "EUR"

def test_format_currency_na():
    assert m.format_currency("", "") == "N/A"

def test_normalize_transaction_json_operationamount_dict_amount_str_to_float():
    tx = {
        "operationAmount": {
            "amount": "1000",
            "currency": {"code": "RUB", "name": "руб."}
        }
    }
    out = m.normalize_transaction(tx)
    assert isinstance(out["operationAmount"]["amount"], float)
    assert out["operationAmount"]["amount"] == 1000.0


def test_normalize_transaction_excel_operationamount_number_assume_rub():
    tx = {"operationAmount": 500}
    out = m.normalize_transaction(tx)
    assert out["operationAmount"]["amount"] == 500.0
    assert out["operationAmount"]["currency"]["code"] == "RUB"

def test_normalize_transaction_csv_builds_operationamount():
    tx = {
        "amount": "130",
        "currency_code": "USD",
        "currency_name": "USD",
    }
    out = m.normalize_transaction(tx)
    assert out["operationAmount"]["amount"] == 130.0
    assert out["operationAmount"]["currency"]["code"] == "USD"
    assert out["operationAmount"]["currency"]["name"] == "USD"

def test_normalize_transaction_empty_dict():
    assert m.normalize_transaction({}) == {}

def test_normalize_transactions_drops_empty():
    txs = [
        {},
        {"amount": "1", "currency_code": "RUB", "currency_name": "руб."}
    ]
    out = m.normalize_transactions(txs)
    assert len(out) == 1

def test_safe_get_date_replaces_z_and_calls_get_date():
    with patch("src.main.get_date", return_value="05.10.2023") as mock_get_date:
        assert m.safe_get_date("2023-10-05T14:30:00Z") == "05.10.2023"
        mock_get_date.assert_called_once_with("2023-10-05T14:30:00+00:00")

def test_format_party_account_prefix_schet():
    with patch("src.main.mask_account_card", return_value="**4321"):
        assert m.format_party("Счет 12345678901234564321") == "Счет **4321"

def test_format_party_card_prefix_type():
    with patch("src.main.mask_account_card", return_value="7771 27** **** 3727"):
        assert (
            m.format_party("MasterCard 7771271234563727")
            == "MasterCard 7771 27** **** 3727"
        )

def test_extract_amount_and_currency_usd():
    tx = {
        "operationAmount": {
            "amount": "130",
            "currency": {"code": "USD", "name": "USD"}
        }
    }
    amount, cur = m.extract_amount_and_currency(tx)
    assert amount == 130.0
    assert cur == "USD"


def test_ask_state_loops_until_valid(capsys):
    with patch("builtins.input", side_effect=["test", "executed"]):
        state = m.ask_state()
        assert state == "EXECUTED"
        out = capsys.readouterr().out
        assert 'Статус операции "test" недоступен.' in out


def test_ask_sort_reverse_invalid_then_valid(capsys):
    with patch("builtins.input", side_effect=["да", "по убыванию"]):
        reverse = m.ask_sort_reverse()
        assert reverse is True
        out = capsys.readouterr().out
        assert "Некорректный выбор" in out

def test_main_happy_path_json_one_result(capsys):
    txs = [
        {
            "id": 1,
            "state": "EXECUTED",
            "date": "2019-12-08T22:46:21.935582",
            "description": "Открытие вклада",
            "to": "Счет 12345678901234564321",
            "operationAmount": {
                "amount": "40542",
                "currency": {"code": "RUB", "name": "руб."}
            },
        }
    ]

    with patch("pathlib.Path.exists", return_value=True), \
            patch("src.main.load_transactions", return_value=txs), \
            patch("src.main.filter_by_state", return_value=txs), \
            patch("src.main.sort_by_date", return_value=txs), \
            patch("src.main.mask_account_card", return_value="**4321"), \
            patch("src.main.get_date", return_value="08.12.2019"), \
            patch("builtins.input", side_effect=[
                "1",  # JSON
                "EXECUTED",  # статус
                "нет",  # сортировка
                "да",  # только рублевые
                "нет",  # поиск
            ]):
        m.main()
    out = capsys.readouterr().out
    assert "Для обработки выбран JSON-файл" in out
    assert 'Операции отфильтрованы по статусу "EXECUTED"' in out
    assert "Всего банковских операций в выборке: 1" in out
    assert "08.12.2019 Открытие вклада" in out
    assert "Счет **4321" in out
    assert "Сумма: 40542 руб." in out


def test_main_empty_selection_prints_message(capsys):
    with patch("pathlib.Path.exists", return_value=True), \
         patch("src.main.load_transactions", return_value=[{"state": "EXECUTED"}]), \
         patch("src.main.filter_by_state", return_value=[]), \
         patch("builtins.input", side_effect=[
             "1",
             "EXECUTED",
             "нет",
             "нет",
             "нет",
         ]):
        m.main()

    out = capsys.readouterr().out
    assert "Не найдено ни одной транзакции" in out


