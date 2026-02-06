import unittest
from unittest.mock import mock_open, patch, MagicMock
from datetime import datetime, time, timedelta



# Импортируем функции из main.py
from src.main import (
    load_json_transactions,
    load_csv_transactions,
    load_xlsx_transactions,
    filter_by_status,
    sort_transactions,
    filter_ruble_transactions,
    search_by_keyword,
    print_transactions,
    main,
    _normalize_cell_value
)


class TestTransactionFunctions(unittest.TestCase):

    def setUp(self):
        """Подготавливаем тестовые данные с корректной структурой."""
        self.transactions = [
            {
                "date": "08.12.2019",
                "description": "Открытие вклада",
                "to": "4321",
                "operationAmount": {
                    "amount": "40542",
                    "currency": {"name": "руб"}
                },
                "state": "EXECUTED"
            },
            {
                "date": "12.11.2019",
                "description": "Перевод с карты на карту",
                "from": "MasterCard 7771 27** **** 3727",
                "to": "Visa Platinum 1293 38** **** 9203",
                "operationAmount": {
                    "amount": "130",
                    "currency": {"name": "USD"}
                },
                "state": "CANCELED"
            },
            {
                "date": "18.07.2018",
                "description": "Перевод организации",
                "from": "Visa Platinum 7492 65** **** 7202",
                "to": "0034",
                "operationAmount": {
                    "amount": "8390",
                    "currency": {"name": "руб"}
                },
                "state": "EXECUTED"
            }
        ]

    # --- Тесты загрузки данных ---

    @patch("builtins.open", new_callable=mock_open, read_data='[{"state": "EXECUTED"}]')
    def test_load_json_transactions(self, mock_file):
        result = load_json_transactions("dummy.json")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["state"], "EXECUTED")

    @patch("builtins.open", new_callable=mock_open, read_data="state,amount\nEXECUTED,100")
    def test_load_csv_transactions(self, mock_file):
        result = load_csv_transactions("dummy.csv")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["state"], "EXECUTED")
        self.assertEqual(result[0]["amount"], "100")

    class TestTransactionFunctions(unittest.TestCase):

        @patch("openpyxl.load_workbook") # ← критично: путь к функции в ВАШЕМ модуле
        def test_load_xlsx_transactions(self, mock_load_workbook):
            # 1. Настраиваем мок для рабочей книги
            mock_wb = MagicMock()
            mock_sheet = MagicMock()
            mock_wb.active = mock_sheet
            mock_load_workbook.return_value = mock_wb  # ← мок возвращает наш mock_wb

            # 2. Имитируем ячейки Excel
            class MockCell:
                def __init__(self, value):
                    self.value = value

            headers = [
                MockCell("date"),
                MockCell("state"),
                MockCell("operationAmount")
            ]
            data_row = [
                MockCell("01.01.2020"),
                MockCell("EXECUTED"),
                MockCell('{"amount": "1000", "currency": {"name": "руб"}}')
            ]

            # 3. Настраиваем поведение моков
            mock_sheet.__getitem__.return_value = headers
            mock_sheet.iter_rows.return_value = iter([data_row])

            # 4. Вызываем тестируемую функцию
            result = load_xlsx_transactions("dummy.xlsx")

            # 5. Проверки
            self.assertEqual(len(result), 1)
            self.assertIn("date", result[0])
            self.assertIn("state", result[0])
            self.assertEqual(result[0]["date"], "01.01.2020")
            self.assertEqual(result[0]["state"], "EXECUTED")
            self.assertIn("operationAmount", result[0])
            self.assertEqual(result[0]["operationAmount"]["amount"], "1000")
            self.assertEqual(
                result[0]["operationAmount"]["currency"]["name"],
                "руб"
            )
    # --- Тесты фильтрации и обработки ---

    def test_filter_by_status_case_insensitive(self):
        """Проверяем фильтрацию по статусу с игнорированием регистра."""
        result = filter_by_status(self.transactions, "executed")
        self.assertEqual(len(result), 2)
        self.assertTrue(all(t["state"] == "EXECUTED" for t in result))

    def test_sort_transactions_ascending(self):
        """Сортировка по дате (возрастание)."""
        result = sort_transactions(self.transactions, ascending=True)
        dates = [t["date"] for t in result]
        expected = ["18.07.2018", "12.11.2019", "08.12.2019"]
        self.assertEqual(dates, expected)

    def test_sort_transactions_descending(self):
        """Сортировка по дате (убывание)."""
        result = sort_transactions(self.transactions, ascending=False)
        dates = [t["date"] for t in result]
        expected = ["08.12.2019", "12.11.2019", "18.07.2018"]
        self.assertEqual(dates, expected)

    def test_filter_ruble_transactions(self):
        """Фильтрация только рублёвых транзакций."""
        result = filter_ruble_transactions(self.transactions)
        self.assertEqual(len(result), 2)
        self.assertTrue(all(
            t["operationAmount"]["currency"]["name"].lower() in ["руб", "rub", "rur"]
            for t in result
        ))

    def test_search_by_keyword(self):
        """Поиск по ключевому слову в описании."""
        result = search_by_keyword(self.transactions, "вклад")
        self.assertEqual(len(result), 1)
        self.assertIn("вклад", result[0]["description"].lower())

        result = search_by_keyword(self.transactions, "перевод")
        self.assertEqual(len(result), 2)

    # --- Тесты вывода ---

    def test_print_transactions_empty(self):
        """Вывод для пустого списка."""
        with patch("builtins.print") as mock_print:
            print_transactions([])
            mock_print.assert_any_call("Не найдено ни одной транзакции, подходящей под ваши условия фильтрации")

    def test_print_transactions_non_empty(self):
        """Вывод непустого списка транзакций."""
        with patch("builtins.print") as mock_print:
            print_transactions(self.transactions[:1])

            # Проверяем ключевые строки вывода
            mock_print.assert_any_call("\nВсего банковских операций в выборке: 1\n")
            mock_print.assert_any_call("08.12.2019 Открытие вклада")
            mock_print.assert_any_call("Счет **4321")
            mock_print.assert_any_call("Сумма: 40542 руб\n")

    # --- Тест main() ---

    def test_main_with_ruble_filter(self):
        """Полный сценарий: загрузка, фильтрация по статусу и валюте."""
        transactions = [
            {
                "id": 1,
                "state": "EXECUTED",
                "date": "2023-01-01T12:00:00",
                "operationAmount": {
                    "amount": "1000.00",
                    "currency": {"name": "руб"}
                },
                "description": "Перевод",
                "from": "Счёт 1234",
                "to": "Счёт 567"
            },
            {
                "id": 2,
                "state": "EXECUTED",
                "date": "2023-01-02T13:00:00",
                "operationAmount": {
                    "amount": "2500.50",
                    "currency": {"name": "руб"}
                },
                "description": "Оплата",
                "from": "Карта 9999",
                "to": "Магазин X"
            },
            {
                "id": 3,
                "state": "EXECUTED",
                "date": "2023-01-03T14:00:00",
                "operationAmount": {
                    "amount": "100.00",
                    "currency": {"name": "USD"}
                },
                "description": "Обмен валюты",
                "from": "Счёт 1111",
                "to": "Банк Y"
            }
        ]

        user_inputs = [
            "1",  # выбор JSON
            "test.json",  # путь к файлу
            "EXECUTED",  # статус для фильтрации
            "нет",  # не сортировать
            "да",  # фильтровать по валюте
            "руб",  # валюта
            "нет"  # не искать по ключевому слову
        ]

        with patch("builtins.input", side_effect=user_inputs):
            with patch("src.main.print_transactions") as mock_print:
                with patch("src.main.load_json_transactions") as mock_load_json:
                    mock_load_json.return_value = transactions

                    print("[ТЕСТ] Начальные транзакции (из load_json_transactions):")
                    for t in transactions:
                        print(
                            f"  ID {t['id']}, статус: {t['state']}, валюта: {t['operationAmount']['currency']['name']}")

                    main()

                    assert mock_print.call_count >= 1, "print_transactions не вызван!"
                    printed_transactions = mock_print.call_args_list[-1][0][0]

                    print(f"[ТЕСТ] Транзакции, переданные в print_transactions: {len(printed_transactions)}")
                    for t in printed_transactions:
                        print(f"  ID {t['id']}, валюта: {t['operationAmount']['currency']['name']}")

                    # Основные проверки
                    assert len(printed_transactions) == 2, (
                        f"Ожидалось 2 рублёвые транзакции, но получено {len(printed_transactions)}"
                    )

                    for t in printed_transactions:
                        assert t["operationAmount"]["currency"]["name"].lower() == "руб", (
                            f"Транзакция ID {t['id']} имеет валюту {t['operationAmount']['currency']['name']}"
                        )

    def test_main_with_keyword_search(self):
        """Тест main() с поиском по ключевому слову."""
        transactions = [
            {
                "id": 1,
                "state": "EXECUTED",
                "date": "2023-01-01T12:00:00",
                "operationAmount": {
                    "amount": "1000.00",
                    "currency": {"name": "руб"}
                },
                "description": "Перевод другу",
                "from": "Счёт 1234",
                "to": "Счёт 5678"
            },
            {
                "id": 2,
                "state": "EXECUTED",
                "date": "2023-01-02T13:00:00",
                "operationAmount": {
                    "amount": "500.00",
                    "currency": {"name": "руб"}
                },
                "description": "Оплата интернета",
                "from": "Карта 9999",
                "to": "Ростелеком"
            }
        ]

        user_inputs = [
            "1", "test.json", "EXECUTED", "нет", "нет", "да", "интернет"
        ]

        with patch("builtins.input", side_effect=user_inputs):
            with patch("src.main.print_transactions") as mock_print:
                with patch("src.main.load_json_transactions") as mock_load_json:
                    mock_load_json.return_value = transactions
                    main()

                    printed_transactions = mock_print.call_args_list[-1][0][0]
                    assert len(printed_transactions) == 1
                    assert "интернет" in printed_transactions[0]["description"].lower()

    def test_main_invalid_choice(self):
        """Тест на неверный выбор формата файла."""
        user_inputs = ["4"]  # неверный пункт меню

        with patch("builtins.input", side_effect=user_inputs):
            with patch("builtins.print") as mock_print:
                main()
                mock_print.assert_any_call("Неверный выбор. Завершение программы.")

    def test_load_json_transactions_not_list(self):
        """JSON содержит не список, а объект — должно вызвать ValueError."""
        with patch("builtins.open", mock_open(read_data='{"key": "value"}')):
            with self.assertRaises(ValueError) as cm:
                load_json_transactions("not_list.json")
            self.assertIn("JSON должен содержать список транзакций", str(cm.exception))

    def test_load_csv_transactions_empty_file(self):
        """Пустой CSV-файл (только заголовки или пусто)."""
        with patch("builtins.open", mock_open(read_data="date,description\n")):
            result = load_csv_transactions("empty.csv")
            self.assertEqual(len(result), 0)

    def test_load_csv_transactions_missing_columns(self):
        """CSV без некоторых ожидаемых колонок."""
        data = "state,amount\nEXECUTED,100"
        with patch("builtins.open", mock_open(read_data=data)):
            result = load_csv_transactions("partial.csv")
            self.assertIn("state", result[0])
            self.assertIn("amount", result[0])
            # Другие поля будут отсутствовать — это нормально

    def test_filter_by_status_missing_state_key(self):
        """Транзакция без поля 'state' — не должна попасть в результат."""
        transactions = [
            {"date": "01.01.2020", "description": "Test"},  # нет state
            {"date": "02.01.2020", "state": "EXECUTED", "description": "OK"}
        ]
        result = filter_by_status(transactions, "EXECUTED")
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0]["state"], "EXECUTED")

    def test_sort_transactions_invalid_date_format(self):
        """Сортировка при невалидном формате даты — должна пропускать или поднимать ошибку."""
        transactions = [
            {"date": "не дата", "description": "Bad"},
            {"date": "01.01.2020", "description": "Good"}
        ]
        # Ожидается, что исключение поднимется при попытке парсинга
        with self.assertRaises(ValueError):
            sort_transactions(transactions, ascending=True)

    def test_filter_ruble_transactions_case_insensitive(self):
        """Фильтрация по валюте с разными регистрами."""
        transactions = [
            {
                "operationAmount": {"currency": {"name": "RUB"}}
            },
            {
                "operationAmount": {"currency": {"name": "rub"}}
            },
            {
                "operationAmount": {"currency": {"name": "RUR"}}
            },
            {
                "operationAmount": {"currency": {"name": "USD"}}
            }
        ]
        result = filter_ruble_transactions(transactions)
        self.assertEqual(len(result), 3)

    def test_search_by_keyword_case_insensitive(self):
        """Поиск по ключевому слову с разным регистром."""
        result = search_by_keyword(self.transactions, "ПЕРЕВОД")
        self.assertEqual(len(result), 2)  # оба перевода найдены

    def test_search_by_keyword_no_match(self):
        """Ключевое слово не найдено — пустой результат."""
        result = search_by_keyword(self.transactions, "ипотека")
        self.assertEqual(len(result), 0)

    def test_search_by_keyword_missing_description(self):
        """Транзакция без описания — не вызывает ошибки."""
        transactions = [
            {"id": 1},  # нет description
            {"id": 2, "description": "платеж"}
        ]
        result = search_by_keyword(transactions, "платеж")
        self.assertEqual(len(result), 1)

    def test_print_transactions_with_missing_fields(self):
        """Вывод транзакции с отсутствующими полями (from, to, amount и т.п.)."""
        transaction = {
            "date": "01.01.2020",
            "description": "Тест",
            # отсутствуют: from, to, operationAmount
        }
        with patch("builtins.print") as mock_print:
            print_transactions([transaction])

            mock_print.assert_any_call("01.01.2020 Тест")
            mock_print.assert_any_call("Сумма:  \n")  # amount и currency пустые

    def test_normalize_cell_value_datetime(self):
        """_normalize_cell_value: преобразование datetime в ISO-строку."""
        dt = datetime(2020, 1, 1, 12, 30, 45)
        self.assertEqual(_normalize_cell_value(dt), "2020-01-01T12:30:45")

    def test_normalize_cell_value_time(self):
        """_normalize_cell_value: преобразование time в HH:MM:SS."""
        t = time(12, 30, 45)
        self.assertEqual(_normalize_cell_value(t), "12:30:45")

    def test_normalize_cell_value_timedelta(self):
        """_normalize_cell_value: timedelta → строка."""
        td = timedelta(hours=1, minutes=30)
        self.assertEqual(_normalize_cell_value(td), "1:30:00")
    if __name__ == "__main__":
        unittest.main()
