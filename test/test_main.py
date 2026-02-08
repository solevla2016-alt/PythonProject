from io import StringIO
from unittest.mock import patch

from src import main as m

import unittest
import json
import os
from pathlib import Path
from tempfile import NamedTemporaryFile

from src.utils import load_transactions
from src.financial_operations_reader import read_csv_file
from src.processing import sort_by_date, filter_by_state



class TestMoreHelpers(unittest.TestCase):
    def test__to_float_none(self):
        self.assertIsNone(m._to_float(None))

    def test__to_float_empty_string(self):
        self.assertIsNone(m._to_float("   "))

    def test__to_float_comma_and_spaces(self):
        self.assertEqual(m._to_float("1 234,50"), 1234.5)

    def test__to_float_invalid(self):
        self.assertIsNone(m._to_float("abc"))

    def test_get_date_simple_yyyy_mm_dd(self):
        self.assertEqual(m.get_date("2023-10-05"), "05.10.2023")

    def test_get_date_unknown_format_returns_original(self):
        self.assertEqual(m.get_date("05/10/2023"), "05/10/2023")

    def test_mask_account_card_schet_with_yo(self):
        self.assertEqual(m.mask_account_card("Счёт 1234567890"), "Счет **7890")

    def test_mask_account_card_20_digits_without_word(self):
        self.assertEqual(
            m.mask_account_card("12345678901234567890"),
            "Счет **7890"
        )

    def test_mask_account_card_too_short_digits(self):
        self.assertEqual(m.mask_account_card("Счет 123"), "None")



class TestNormalizeTransaction(unittest.TestCase):
    def test_normalize_transaction_operationAmount_dict_amount_str_to_float(self):
        tx = {
            "operationAmount": {
                "amount": "1000.50",
                "currency": {"code": "USD", "name": "USD"}
            }
        }
        out = m.normalize_transaction(tx)
        self.assertIsInstance(out["operationAmount"]["amount"], float)
        self.assertEqual(out["operationAmount"]["amount"], 1000.5)

    def test_normalize_transaction_operationAmount_str_to_float(self):
        tx = {"operationAmount": "2000"}
        out = m.normalize_transaction(tx)
        self.assertEqual(out["operationAmount"], 2000.0)

    def test_normalize_transaction_csv_shape_builds_operationAmount(self):
        tx = {
            "amount": "130",
            "currency_code": "USD",
            "currency_name": "USD",
            "description": "Перевод"
        }
        out = m.normalize_transaction(tx)
        self.assertIsInstance(out["operationAmount"], dict)
        self.assertEqual(out["operationAmount"]["amount"], 130.0)
        self.assertEqual(out["operationAmount"]["currency"]["code"], "USD")
        self.assertEqual(out["operationAmount"]["currency"]["name"], "USD")

    def test_normalize_transactions_drops_empty_dicts(self):
        txs = [
            {},
            {"amount": "10", "currency_code": "RUB", "currency_name": "руб."}
        ]
        out = m.normalize_transactions(txs)
        self.assertEqual(len(out), 1)



class TestSearchAndSortHelpers(unittest.TestCase):
    def test_filter_by_description_keyword_empty_keyword_returns_same(self):
        txs = [{"description": "Перевод"}, {"description": "Открытие вклада"}]
        out = m.filter_by_description_keyword(txs, "")
        self.assertEqual(out, txs)

    def test_filter_by_description_keyword_finds_case_insensitive(self):
        txs = [
            {"description": "Перевод организации"},
            {"description": "Открытие вклада"}
        ]
        out = m.filter_by_description_keyword(txs, "ОРГАНИЗАЦИИ")
        self.assertEqual(len(out), 1)
        self.assertEqual(out[0]["description"], "Перевод организации")

    @patch("builtins.input", side_effect=["что-то", "1"])
    def test_ask_sort_reverse_loops_until_valid(self, mock_input):
        rev = m.ask_sort_reverse()
        self.assertFalse(rev)

    @patch("builtins.input", side_effect=["x", "2"])
    def test_ask_sort_reverse_choose_desc(self, mock_input):
        rev = m.ask_sort_reverse()
        self.assertTrue(rev)



class TestMainMoreBranches(unittest.TestCase):
    @patch("pathlib.Path.exists", return_value=True)
    @patch("src.main.sort_by_date")
    @patch("src.main.filter_by_state")
    @patch("src.main.load_transactions")
    @patch("builtins.input")
    def test_main_rub_filter_keeps_only_rub(
        self,
        mock_input,
        mock_load_transactions,
        mock_filter_by_state,
        mock_sort_by_date,
        mock_exists,
    ):
        txs = [
            {
                "id": 1,
                "date": "2019-12-08T22:46:21.935582",
                "description": "Открытие вклада",
                "to": "Счет 12345678901234564321",
                "operationAmount": {
                    "amount": "40542",
                    "currency": {"code": "RUB", "name": "руб."}
                },
                "state": "EXECUTED",
            },
            {
                "id": 2,
                "date": "2019-12-07T22:46:21.935582",
                "description": "Открытие вклада",
                "to": "Счет 12345678901234560034",
                "operationAmount": {
                    "amount": "10",
                    "currency": {"code": "USD", "name": "USD"}
                },
                "state": "EXECUTED",
            },
        ]

        mock_load_transactions.return_value = txs
        mock_filter_by_state.return_value = txs
        mock_sort_by_date.return_value = txs
        mock_input.side_effect = [
            "1",          # JSON
            "EXECUTED",   # статус
            "нет",        # сортировать
            "да",         # только рублёвые
            "нет",        # фильтр по слову
        ]
        with patch("sys.stdout", new_callable=StringIO) as fake_out:
            m.main()
            output = fake_out.getvalue()
        self.assertIn("Всего банковских операций в выборке: 1", output)
        self.assertIn("Сумма: 40542 руб.", output)
        self.assertNotIn("USD", output)

    @patch("pathlib.Path.exists", return_value=True)
    @patch("src.main.sort_by_date")
    @patch("src.main.filter_by_state")
    @patch("src.main.load_transactions")
    @patch("builtins.input")
    def test_main_search_filter_reduces_list(
        self,
        mock_input,
        mock_load_transactions,
        mock_filter_by_state,
        mock_sort_by_date,
        mock_exists,
    ):
        txs = [
            {
                "id": 1,
                "date": "2019-11-12T10:00:00",
                "description": "Перевод с карты на карту",
                "from": "MasterCard 7771271234",
                "from": "MasterCard 7771271234563727",
                "to": "Visa Platinum 1293381234569203",
                "operationAmount": {
                    "amount": "130",
                    "currency": {"code": "USD", "name": "USD"}
                },
                "state": "CANCELED",
            },
            {
                "id": 2,
                "date": "2019-11-12T11:00:00",
                "description": "Открытие вклада",
                "to": "Счет 12345678901234564321",
                "operationAmount": {
                    "amount": "1",
                    "currency": {"code": "RUB", "name": "руб."}
                },
                "state": "CANCELED",
            },
        ]
        mock_load_transactions.return_value = txs
        mock_filter_by_state.return_value = txs
        mock_sort_by_date.return_value = txs
        mock_input.side_effect = [
            "1",          # JSON
            "CANCELED",   # статус
            "нет",        # сортировать
            "нет",        # только рублёвые
            "да",         # фильтр по слову
            "карты",      # ключевое слово
        ]
        with patch("sys.stdout", new_callable=StringIO) as fake_out:
            m.main()
            output = fake_out.getvalue()
        self.assertIn("Всего банковских операций в выборке: 1", output)
        self.assertIn("Перевод с карты на карту", output)
        self.assertNotIn("Открытие вклада", output)



class TestLoadTransactionsJson(unittest.TestCase):
    def test_load_json_transactions(self):
        tmp = NamedTemporaryFile(mode="w", suffix=".json", delete=False, encoding="utf-8")
        try:
            json.dump([{"id": 1, "amount": 100}], tmp, ensure_ascii=False)
            tmp.close()

            txs = load_transactions(Path(tmp.name))
            self.assertEqual(len(txs), 1)
            self.assertEqual(txs[0]["id"], 1)
            self.assertEqual(txs[0]["amount"], 100)
        finally:
            os.unlink(tmp.name)

    def test_load_nonexistent_file_raises_or_empty(self):
        p = Path("definitely_not_exists_12345.json")
        try:
            txs = load_transactions(p)
        except FileNotFoundError:
            return
        self.assertEqual(txs, [])



class TestReadCsvFile(unittest.TestCase):
    def test_read_csv_file_reads_semicolon_csv(self):
        tmp = NamedTemporaryFile(mode="w", suffix=".csv", delete=False, encoding="utf-8")
        try:
            tmp.write("id;state;date;amount;currency_name;currency_code;from;to;description\n")
            tmp.write("1;CANCELED;2019-11-12T10:00:00;130;USD;USD;MasterCard 7771271234563727;Visa Platinum 1293381234569203;Перевод с карты на карту\n")
            tmp.close()

            txs = read_csv_file(tmp.name)
            self.assertEqual(len(txs), 1)
            self.assertEqual(txs[0]["id"], 1)
            self.assertEqual(txs[0]["currency_code"], "USD")
            self.assertEqual(txs[0]["amount"], 130)
        finally:
            os.unlink(tmp.name)



class TestSortByDate(unittest.TestCase):
    def test_sort_by_date_ascending(self):
        txs = [
            {"date": "2023-01-01T12:00:00"},
            {"date": "2022-01-01T12:00:00"},
            {"date": "2024-01-01T12:00:00"}
        ]
        sorted_txs = m.sort_by_date(txs, reverse=False)
        self.assertEqual(sorted_txs[0]["date"], "2022-01-01T12:00:00")
        self.assertEqual(sorted_txs[1]["date"], "2023-01-01T12:00:00")
        self.assertEqual(sorted_txs[2]["date"], "2024-01-01T12:00:00")

    def test_sort_by_date_descending(self):
        txs = [
            {"date": "2023-01-01T12:00:00"},
            {"date": "2022-01-01T12:00:00"},
            {"date": "2024-01-01T12:00:00"}
        ]
        sorted_txs = m.sort_by_date(txs, reverse=True)
        self.assertEqual(sorted_txs[0]["date"], "2024-01-01T12:00:00")
        self.assertEqual(sorted_txs[1]["date"], "2023-01-01T12:00:00")
        self.assertEqual(sorted_txs[2]["date"], "2022-01-01T12:00:00")



class TestFilterByState(unittest.TestCase):
    def test_filter_by_state_executed(self):
        txs = [
            {"state": "EXECUTED"},
            {"state": "CANCELED"},
            {"state": "EXECUTED"}
        ]
        filtered = filter_by_state(txs, "EXECUTED")
        self.assertEqual(len(filtered), 2)
        self.assertTrue(all(tx["state"] == "EXECUTED" for tx in filtered))

    def test_filter_by_state_unknown_returns_empty_or_original(self):
        txs = [{"state": "EXECUTED"}, {"state": "CANCELED"}]
        filtered = filter_by_state(txs, "UNKNOWN_STATE")
        self.assertTrue(filtered == [] or filtered == txs)


if __name__ == "__main__":
    unittest.main()


