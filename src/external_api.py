import os
import requests
from typing import Dict, Union
from dotenv import load_dotenv

# 1. Загружаем .env из корневой директории
dotenv_path = os.path.join(os.path.dirname(__file__), "..", ".env")
load_dotenv(dotenv_path)

# 2. Отладка: проверяем загрузку ключа
print("→ Проверка окружения:")
api_key = os.getenv("API_KEY")
if api_key:
    print(f"  API_KEY загружен (длина: {len(api_key)})")
    print(f"  Пример: {api_key[:4]}...{api_key[-4:]}")
else:
    print("  ERROR: API_KEY не найден в .env!")

print("-" * 40)


def convert_to_rubles(amount: float, currency: str) -> float:
    """Конвертирует сумму из валюты в RUB через APILayer."""
    api_key = os.getenv("API_KEY")

    if not api_key:
        raise ValueError("API_KEY не найден в .env. Убедитесь, что файл .env существует и содержит API_KEY.")

    url = "https://api.apilayer.com/exchangerates_data/convert"


    params: Dict[str, str] = {
        "from": str(currency),
        "to": "RUB",
        "amount": str(float(amount))
    }
    headers: Dict[str, str] = {"apikey": api_key}

    try:
        response = requests.get(url, params=params, headers=headers, timeout=5)
        response.raise_for_status()
        data = response.json()

        if not data.get("success"):
            err_info = data.get("error", {}).get("info", "Неизвестная ошибка")
            raise Exception(f"API ошибка: {err_info}")

        converted_amount = float(data["result"])
        return round(converted_amount, 2)

    except requests.exceptions.RequestException as e:
        raise Exception(f"Сеть/запрос ошибка: {e}")


def process_transaction(transaction: Dict[str, Union[float, str]]) -> float:
    """Обрабатывает транзакцию и возвращает сумму в рублях."""

    amount_value = transaction["amount"]
    if isinstance(amount_value, (int, float)):
        amount = float(amount_value)
    elif isinstance(amount_value, str):
        try:
            amount = float(amount_value)
        except ValueError:
            raise ValueError(f"amount должен быть числом, получено: {amount_value}")
    else:
        raise TypeError(f"amount должен быть числом или строкой, получено: {type(amount_value)}")


    currency_value = transaction["currency"]
    if not isinstance(currency_value, str):
        raise TypeError(
            f"currency должно быть строкой, получено: {type(currency_value)}"
        )
    currency = currency_value.upper().strip()

    if currency == "RUB":
        return amount

    if currency not in ("USD", "EUR"):
        raise ValueError(
            f"Валюта {currency} не поддерживается. Используйте USD, EUR, RUB."
        )

    return convert_to_rubles(amount, currency)
