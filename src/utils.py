import json
import logging
import os
from typing import Any, Dict, List

# print("=== Скрипт запущен! ===")

# Отладка: проверим окружение
# print("=== ОТЛАДКА ===")
# print(f"Текущий каталог: {os.getcwd()}")
# print(f"Существует logs/? {os.path.exists('logs')}")

# Создаём директорию для логов
os.makedirs("logs", exist_ok=True)

# Создаём отдельный логер для модуля utils
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # Уровень не ниже DEBUG

# Настраиваем FileHandler для логера модуля utils
file_handler = logging.FileHandler("logs/utils.log", mode="w", encoding="utf-8")

# Настраиваем StreamHandler для вывода в консоль
stream_handler = logging.StreamHandler()

# Создаём форматер (file_formatter) с требуемым форматом
formatter = logging.Formatter(
    "%(asctime)s [%(module)s:%(lineno)d][%(levelname)s]: %(message)s"
)

# Устанавливаем форматер для обоих обработчиков
file_handler.setFormatter(formatter)
stream_handler.setFormatter(formatter)

# Добавляем обработчики к логеру модуля utils
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

# print(f"Обработчики логгера: {logger.handlers}")
# print(f"Уровень логгера: {logger.level}")


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """Загружает список словарей с данными о финансовых транзакциях из JSON-файла."""
    logger.debug("Функция load_transactions вызвана!")

    try:
        if not os.path.exists(file_path):
            logger.warning(f"Файл не найден: {file_path}")
            return []

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            logger.debug(f"Загружено из файла: {data}")

        if isinstance(data, list):
            logger.info("Данные загружены успешно.")
            return data
        else:
            logger.error(f"Данные не являются списком (тип: {type(data)})")
            return []

    except FileNotFoundError:
        logger.error(f"FileNotFoundError: файл не найден — {file_path}")
        return []
    except PermissionError:
        logger.error(f"PermissionError: нет доступа к файлу — {file_path}")
        return []
    except json.JSONDecodeError as e:
        logger.error(f"JSONDecodeError: ошибка парсинга JSON — {e}")
        return []
    except UnicodeDecodeError as e:
        logger.error(f"UnicodeDecodeError: ошибка кодировки файла — {e}")
        return []
    except Exception as e:
        logger.critical(f"Неожиданная ошибка: {type(e).__name__}: {e}")
        return []


# Тестовый вызов
if __name__ == "__main__":
    result = load_transactions("data.json")
    print(f"Результат загрузки: {result}")
