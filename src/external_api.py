import os
from functools import lru_cache
from typing import Any, Dict

import requests
from dotenv import load_dotenv

load_dotenv()

# Получение и проверка API_KEY
API_KEY = os.getenv("API_KEY")
if not API_KEY:
    raise ValueError("API_KEY не найден в .env. Создайте файл .env с API_KEY=ваш_ключ.")


BASE_URL = "https://api.apilayer.com/exchangerates_data/convert"


@lru_cache(maxsize=128)
def _get_exchange_rate(from_currency: str, to_currency: str) -> float:
    """Получает курс конвертации с кешированием."""
    params = {"from": from_currency, "to": to_currency, "amount": str(1)}
    headers = {"apikey": API_KEY}

    for attempt in range(2):
        try:
            response = requests.get(
                BASE_URL, params=params, headers=headers, timeout=10
            )
            response.raise_for_status()
            data = response.json()

            if isinstance(data, dict) and "error" in data:
                error_info = data["error"].get("info", "Неизвестная ошибка")
                raise Exception(f"API ошибка: {error_info}")
            elif not isinstance(data, dict):
                raise Exception("Неверный формат ответа API")

            return float(data["result"])

        except requests.exceptions.RequestException as e:
            if attempt == 1:
                raise Exception(f"Ошибка запроса к API после 2 попыток: {e}")
            continue

    raise Exception("Не удалось получить курс конвертации после 2 попыток")


def convert_to_rubles(amount: float, currency: str) -> float:
    """Конвертирует сумму из валюты в RUB через APILayer."""
    try:
        rate = _get_exchange_rate(currency, "RUB")
        converted = amount * rate
        return round(converted, 2)
    except requests.exceptions.RequestException as e:
        raise RuntimeError(f"Сетевой сбой при запросе курса {currency}→RUB: {e}") from e
    except Exception as e:
        raise RuntimeError(f"Ошибка получения курса {currency}→RUB: {e}") from e


def process_transaction(transaction: Dict[str, Any]) -> float:
    """Обрабатывает транзакцию и возвращает сумму в рублях."""

    # Проверка наличия обязательных ключей
    if "operationAmount" not in transaction:
        raise KeyError("Поле 'operationAmount' отсутствует в транзакции.")

    if "amount" not in transaction["operationAmount"]:
        raise KeyError("Поле 'operationAmount.amount' отсутствует в транзакции.")
    if "currency" not in transaction["operationAmount"]:
        raise KeyError("Поле 'operationAmount.currency' отсутствует в транзакции.")
    if "code" not in transaction["operationAmount"]["currency"]:
        raise KeyError("Поле 'operationAmount.currency.code' отсутствует в транзакции.")

    # Извлечение данных
    amount_value = transaction["operationAmount"]["amount"]
    currency_code = transaction["operationAmount"]["currency"]["code"]

    # Валидация amount
    if isinstance(amount_value, (int, float)):
        amount = float(amount_value)
    elif isinstance(amount_value, str):
        amount_str = amount_value.strip()
        if not amount_str:
            raise ValueError(
                "Поле 'operationAmount.amount' не может быть пустой строкой."
            )
        try:
            amount = float(amount_str)
        except ValueError:
            raise ValueError(
                f"Поле 'operationAmount.amount' должно быть числом, получено: {amount_value}"
            )
    else:
        raise TypeError(
            f"Поле 'operationAmount.amount' должно быть числом или строкой, получено: {type(amount_value).__name__}"
        )

    if amount < 0:
        raise ValueError(
            f"Поле 'operationAmount.amount' не может быть отрицательным: {amount}"
        )

    # Валидация currency.code
    if not isinstance(currency_code, str):
        raise TypeError(
            f"Поле 'operationAmount.currency.code' должно быть строкой, получено: {type(currency_code).__name__}"
        )

    currency = currency_code.strip().upper()
    if not currency:
        raise ValueError(
            "Поле 'operationAmount.currency.code' не может быть пустой строкой."
        )

    SUPPORTED_CURRENCIES = {"RUB", "USD", "EUR"}
    if currency not in SUPPORTED_CURRENCIES:
        raise ValueError(
            f"Валюта {currency} не поддерживается. Используйте: {SUPPORTED_CURRENCIES}."
        )

    return convert_to_rubles(amount, currency)
