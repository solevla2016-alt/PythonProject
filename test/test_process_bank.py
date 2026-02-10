import unittest
from src.process_bank import process_bank_search, process_bank_operations


class TestProcessBankSearch(unittest.TestCase):
    def setUp(self):
        self.test_data = [
            {"id": 1, "amount": 1000, "description": "Оплата телефона"},
            {"id": 2, "amount": 2000, "description": "Пополнение счета"},
            {"id": 3, "amount": 500, "description": "Покупка продуктов"},
            {"id": 4, "amount": 700, "description": "Перевод другу"},
        ]

    def test_found_match(self):
        result = process_bank_search(self.test_data, "телеф")
        expected = [{"id": 1, "amount": 1000, "description": "Оплата телефона"}]
        self.assertEqual(result, expected)

    def test_no_matches(self):
        result = process_bank_search(self.test_data, "машина")
        self.assertEqual(result, [])

    def test_empty_data(self):
        result = process_bank_search([], "любое_слово")
        self.assertEqual(result, [])

    def test_empty_query(self):
        result = process_bank_search(self.test_data, "")
        self.assertEqual(result, self.test_data)

    def test_case_insensitive_search(self):
        result = process_bank_search(self.test_data, "пополнение")
        expected = [{"id": 2, "amount": 2000, "description": "Пополнение счета"}]
        self.assertEqual(result, expected)

    def test_special_chars_in_query(self):
        """Тест: запрос содержит спецсимволы (экранируются)."""
        result = process_bank_search(self.test_data, "тел.+фон")
        # Без re.escape "тел.+фон" искало бы "тел", затем любой символ, затем "фон"
        # С re.escape ищет буквально "тел.+фон" → не находит
        self.assertEqual(result, [])


    def test_regex_literal_search(self):
        """Тест: если убрать re.escape, можно было бы искать по шаблону."""
        # В текущей реализации это не поддерживается (намеренно)
        pass



class TestProcessBankOperations(unittest.TestCase):
    def setUp(self):
        self.test_data = [
            {"id": 1, "amount": 1000, "description": "Оплата телефона МТС"},
            {"id": 2, "amount": 2000, "description": "Пополнение счёта через банкомат"},
            {"id": 3, "amount": 500, "description": "Покупка продуктов в магазине"},
            {"id": 4, "amount": 300, "description": "Оплата интернета"},
            {"id": 5, "amount": 1500, "description": "Перевод зарплаты"},
        ]

    def test_count_categories(self):
        categories = ["телефон", "продукты", "зарплата"]
        result = process_bank_operations(self.test_data, categories)
        expected = {"телефон": 1}
        self.assertEqual(result, expected)

    def test_no_matching_categories(self):
        categories = ["машина", "отдых"]
        result = process_bank_operations(self.test_data, categories)
        self.assertEqual(result, {})

    def test_empty_transactions(self):
        categories = ["телефон"]
        result = process_bank_operations([], categories)
        self.assertEqual(result, {})

    def test_multiple_matches_one_category(self):
        # Транзакция учитывается только по первой подходящей категории
        categories = ["оплата", "перевод"]
        result = process_bank_operations(self.test_data, categories)
        # "Оплата телефона" и "Оплата интернета" → категория "оплата"
        # "Перевод зарплаты" → категория "перевод"
        expected = {"оплата": 2, "перевод": 1}
        self.assertEqual(result, expected)

    def test_case_insensitive_category(self):
        # Определяем список категорий, которые ищем
        categories = ["ТЕЛЕФОН", "ПРОДУКТЫ", "РАЗВЛЕЧЕНИЯ"]  # ← добавьте эту строку!

        # Ожидаемый результат: только "ТЕЛЕФОН" должен быть найден (1 транзакция)
        expected = {"ТЕЛЕФОН": 1}

        # Вызываем тестируемую функцию
        result = process_bank_operations(self.test_data, categories)

        # Проверяем результат
        self.assertEqual(result, expected)


if __name__ == "__main__":
    unittest.main()