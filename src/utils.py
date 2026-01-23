import json
import os
from typing import Any, Dict, List


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Загружает список словарей с данными о финансовых транзакциях из JSON‑файла.

    """
    try:
        if not os.path.exists(file_path):
            print(f"[DEBUG] Файл не найден: {file_path}")
            return []

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)
            print(f"[DEBUG] Загружено из файла: {data}")

        if isinstance(data, list):
            return data
        else:
            print(f"[DEBUG] Данные не являются списком (тип: {type(data)})")
            return []

    except FileNotFoundError:
        print(f"[DEBUG] FileNotFoundError: файл не найден — {file_path}")
        return []

    except PermissionError:
        print(f"[DEBUG] PermissionError: нет доступа к файлу — {file_path}")
        return []

    except json.JSONDecodeError as e:
        print(f"[DEBUG] JSONDecodeError: ошибка парсинга JSON — {e}")
        return []

    except UnicodeDecodeError as e:
        print(f"[DEBUG] UnicodeDecodeError: ошибка кодировки файла — {e}")
        return []

    except Exception as e:
        print(f"[DEBUG] Неожиданная ошибка: {type(e).__name__}: {e}")
        return []
