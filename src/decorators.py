import functools
from datetime import datetime
from typing import Callable, Any, Optional


def log(filename: Optional[str] = None) -> Callable:
    """Декоратор для логирования начала и конца выполнения функции, а также результатов или возникающих ошибок.

    Аргументы:
        filename (str, optional): Имя файла, в который будут записаны логи. По умолчанию None,
        что означает вывод в консоль.

           Возможные сценарии использования:
        - Простое ведение журнала всех вызовов функций.
        - Анализ поведения программы и диагностика ошибок.
    """

    def decorator(func: Callable) -> Callable:
        """Обертка над оригинальной функцией."""

        @functools.wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> Any:
            """Основная логика выполнения декорированной функции с обработкой логов."""
            try:
                # Выполняем оригинальную функцию и получаем результат
                result = func(*args, **kwargs)

                # Создаем сообщение о результате
                message = f"{func.__name__}: {result}"

                # Записываем лог в файл или выводим в консоль
                if filename:
                    with open(filename, mode="a", encoding="utf-8") as file:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        file.write(f"[{timestamp}] {message}\n")
                else:
                    print(message)

                return result

            except Exception as e:
                # Сообщение об ошибке с указанием имени функции, типа ошибки и входных параметров
                err_message = f"{func.__name__}: error: {type(e).__name__}. Inputs: {args}, {kwargs}"

                # Записываем ошибку в файл или выводим в консоль
                if filename:
                    with open(filename, mode="a", encoding="utf-8") as file:
                        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                        file.write(f"[{timestamp}] {err_message}\n")
                else:
                    print(err_message)

        return wrapper

    return decorator
