import unittest
import os
from io import StringIO
from contextlib import redirect_stdout
from datetime import datetime


from src.decorators import log

class TestLogDecorator(unittest.TestCase):
    def setUp(self):
        self.test_file_name = "test_log.txt"
        if os.path.exists(self.test_file_name):
            os.remove(self.test_file_name)

    def tearDown(self):
        if os.path.exists(self.test_file_name):
            os.remove(self.test_file_name)

    def test_successful_execution_console_output(self):
        """Тестируем успешное выполнение функции с выводом в консоль"""
        output = StringIO()  # Перенаправляем stdout для захвата вывода

        @log()
        def successful_func():
            return "OK"

        with redirect_stdout(output):
            successful_func()

        # Проверяем содержимое консоли
        captured_output = output.getvalue().strip()
        expected_result = f'successful_func: OK'
        self.assertIn(expected_result, captured_output)

    def test_error_handling_console_output(self):
        """Тестируем возникновение ошибки с выводом в консоль"""
        output = StringIO()  # Перенаправляем stdout для захвата вывода

        @log()
        def failing_func():
            raise ValueError("Test Error")

        with redirect_stdout(output):
            try:
                failing_func()
            except ValueError:
                pass

        # Проверяем содержимое консоли
        captured_output = output.getvalue().strip()
        expected_result = f'failing_func: error: ValueError. Inputs: (), {{}}'
        self.assertIn(expected_result, captured_output)

    def test_successful_execution_file_logging(self):
        """Тестируем успешное выполнение функции с логированием в файл"""
        @log(filename=self.test_file_name)
        def successful_func():
            return "OK"

        successful_func()

        # Читаем содержимое файла
        with open(self.test_file_name, 'r', encoding='utf-8') as file:
            content = file.read().strip()

        expected_result = f'successful_func: OK'
        self.assertIn(expected_result, content)

    def test_error_handling_file_logging(self):
        """Тестируем возникновение ошибки с логированием в файл"""
        @log(filename=self.test_file_name)
        def failing_func():
            raise TypeError("Test Error")

        try:
            failing_func()
        except TypeError:
            pass

        # Читаем содержимое файла
        with open(self.test_file_name, 'r', encoding='utf-8') as file:
            content = file.read().strip()

        expected_result = f'failing_func: error: TypeError. Inputs: (), {{}}'
        self.assertIn(expected_result, content)

if __name__ == '__main__':
    unittest.main()