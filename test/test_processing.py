import pytest
from src.processing import filter_by_state, sort_by_date

data = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
]

@pytest.mark.parametrize('state, expected_length', [
    ("EXECUTED", 2),
    ("CANCELED", 2),
    ("UNKNOWN", 0),
])
def test_filter_by_state(state, expected_length):
    filtered_data = filter_by_state(data, state)
    assert len(filtered_data) == expected_length




data = [
    {"id": 41428829, "state": "EXECUTED", "date": "2019-07-03T18:35:29.512364"},
    {"id": 615064591, "state": "CANCELED", "date": "2018-10-14T08:21:33.419441"},
    {"id": 594226727, "state": "CANCELED", "date": "2018-09-12T21:27:25.241689"},
    {"id": 939719570, "state": "EXECUTED", "date": "2018-06-30T02:08:58.425572"},
]

@pytest.mark.parametrize('reverse, expected_order', [
    (True, ["2019-07-03", "2018-10-14", "2018-09-12", "2018-06-30"]),
    (False, ["2018-06-30", "2018-09-12", "2018-10-14", "2019-07-03"]),
])
def test_sort_by_date(reverse, expected_order):
    sorted_data = sort_by_date(data, reverse)
    actual_dates = [item['date'].split('T')[0] for item in sorted_data]
    assert actual_dates == expected_order