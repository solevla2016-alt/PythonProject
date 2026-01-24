import pytest
from datetime import datetime
from src.processing import filter_by_state, sort_by_date  # Подставьте ваш реальный путь импорта!

# Тестируем фильтрацию по состоянию
@pytest.mark.parametrize("input_data,state,expected_result", [
    ([{"id": 1, "state": "EXECUTED"}, {"id": 2, "state": "PENDING"}],
     "EXECUTED",
     [{"id": 1, "state": "EXECUTED"}]),

    ([{"id": 1, "state": "CANCELED"}, {"id": 2, "state": "EXECUTED"}],
     "CANCELED",
     [{"id": 1, "state": "CANCELED"}]),

    ([], "EXECUTED", []),
])
def test_filter_by_state(input_data, state, expected_result):
    result = filter_by_state(input_data, state)
    assert result == expected_result


# Тестируем сортировку по дате
@pytest.mark.parametrize("transactions,reverse,expected_order", [
    ([
        {"id": 1, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 2, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"}
    ], True, ["2019-07-03", "2018-06-30"]),

    ([
        {"id": 1, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
        {"id": 2, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"}
    ], False, ["2018-06-30", "2019-07-03"]),

    ([], True, [])
])
def test_sort_by_date(transactions, reverse, expected_order):
    sorted_transactions = sort_by_date(transactions, reverse)
    actual_dates = [datetime.strptime(t['date'].split('T')[0], '%Y-%m-%d').strftime('%Y-%m-%d') for t in sorted_transactions]
    assert actual_dates == expected_order