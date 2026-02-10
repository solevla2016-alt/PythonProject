import re
from collections import Counter
from typing import Any, Dict, List


def process_bank_search(
    transactions: List[Dict[str, Any]], query: str
) -> List[Dict[str, Any]]:
    """Фильтрует список банковских транзакций по поисковому запросу в описании"""
    if not query:
        return transactions
    pattern = re.escape(query)
    compiled = re.compile(pattern, re.IGNORECASE)
    return [t for t in transactions if compiled.search(t.get("description", ""))]


def process_bank_operations(
    transactions: List[Dict[str, Any]], categories: List[str]
) -> Dict[str, int]:
    """Подсчитывает количество транзакций по заданным категориям."""
    counter: Counter[str] = Counter()  # Явная аннотация типа

    for transaction in transactions:
        desc = transaction.get("description", "").lower()

        for category in categories:
            if category.lower() in desc:
                counter[category] += 1

    return dict(counter)
