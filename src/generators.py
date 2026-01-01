from typing import Dict, List, Iterator, Any

def filter_by_currency(transactions: List[Dict[str, Any]], currency_code: str) -> Iterator[Dict[str, Any]]:
    """
    Возвращает итератор, выдающий транзакции с указанной валютой.
    """
    for transaction in transactions:
        if (
            transaction.get("operationAmount", {})
              .get("currency", {})
              .get("code") == currency_code
        ):
            yield transaction


if __name__ == "__main__":

    transactions = [
        {
            "id": 939719570,
            "state": "EXECUTED",
            "date": "2018-06-30T02:08:58.425572",
            "operationAmount": {
                "amount": "9824.07",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод организации",
            "from": "Счет 75106830613657916952",
            "to": "Счет 11776614605963066702",
        },
        {
            "id": 142264268,
            "state": "EXECUTED",
            "date": "2019-04-04T23:20:05.206878",
            "operationAmount": {
                "amount": "79114.93",
                "currency": {"name": "USD", "code": "USD"},
            },
            "description": "Перевод со счета на счет",
            "from": "Счет 19708645243227258542",
            "to": "Счет 75651667383060284188",
        },
    ]

    usd_transactions = filter_by_currency(transactions, "USD")
    for _ in range(2):
        print(next(usd_transactions))


def transaction_descriptions(transactions: List[Dict[str, Any]]) -> Iterator[str]:
    """
    Генерирует последовательность описаний транзакций.
    """
    for transaction in transactions:
        yield transaction["description"]


def card_number_generator(start: int, end: int) -> Iterator[str]:
    """
    Генератор, выдающий номера банковских карт в формате XXXX XXXX XXXX XXXX.
    """
    for number in range(start, end + 1):
        formatted_card = f"{number:016d}"
        yield " ".join([formatted_card[i:i+4] for i in range(0, 16, 4)])
