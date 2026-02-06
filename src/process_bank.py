import re
from collections import Counter
from typing import Any, Dict, List


def process_bank_search(
    transactions: List[Dict[str, Any]], query: str
) -> List[Dict[str, Any]]:
    if not query:
        return transactions
    pattern = re.escape(query)
    compiled = re.compile(pattern, re.IGNORECASE)
    return [t for t in transactions if compiled.search(t.get("description", ""))]


def process_bank_operations(
    transactions: List[Dict[str, Any]], categories: List[str]
) -> Dict[str, int]:
    matched_descriptions = []
    for transaction in transactions:
        desc = transaction.get("description", "").lower()
        for category in categories:
            if category.lower() in desc:
                matched_descriptions.append(category)
                break
    return dict(Counter(matched_descriptions))
