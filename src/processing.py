from datetime import datetime


def filter_by_state(dict_lists: list, state: str = "EXECUTED") -> list:
    """
    Реализована функция, которая принимает список словарей и опционально значение для ключа
    state (по умолчанию 'EXECUTED'). Возвращает список словарей, у которых значение ключа
    'state' совпадает с указанным параметром.
    """
    return [dict_list for dict_list in dict_lists if dict_list.get("state") == state]


if __name__ == "__main__":  # pragma: no cover
    data = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    ]
    print(filter_by_state(data))


def sort_by_date(transactions: list, reverse: bool = True) -> list:
    """
    Сортирует список транзакций по дате, используя указанный порядок сортировки.
    """
    # Преобразование строковых значений дат в объекты datetime для правильной сортировки
    sorted_transactions = sorted(
        transactions,
        key=lambda x: datetime.strptime(x["date"].split("T")[0], "%Y-%m-%d"),
        reverse=reverse,
    )
    return sorted_transactions


if __name__ == "__main__":  # pragma: no cover
    data = [
        {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
        {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
        {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    ]
    print(sort_by_date(data))
