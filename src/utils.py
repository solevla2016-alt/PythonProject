import json
import os
from typing import Any, Dict, List


def load_transactions(file_path: str) -> List[Dict[str, Any]]:
    """
    Функция загружает список словарей с информацией о финансовых операциях из JSON-файла.

    """
    try:
        # Проверяем наличие файла
        if not os.path.exists(file_path):
            return []

        with open(file_path, "r", encoding="utf-8") as f:
            data = json.load(f)

        if isinstance(data, list):
            return data
        else:
            return []
    except Exception as e:
        print(f"Ошибка загрузки данных: {e}")
        return []
