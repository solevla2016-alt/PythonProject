import pytest

from src.processing import filter_by_state, sort_by_date


@pytest.mark.parametrize(
    "state, expected_length",
    [
        ("EXECUTED", 2),
        ("CANCELED", 1),
        ("UNKNOWN", 0),
    ],
)
def test_filter_by_state(transactions_data, state, expected_length):
    filtered_data = filter_by_state(transactions_data, state)
    assert len(filtered_data) == expected_length


@pytest.mark.parametrize(
    "reverse, expected_order",
    [
        (True, ["2019-07-03", "2018-10-14", "2018-06-30"]),
        (False, ["2018-06-30", "2018-10-14", "2019-07-03"]),
    ],
)
def test_sort_by_date(transactions_data, reverse, expected_order):
    # Передаём transactions_data в функцию sort_by_date
    sorted_data = sort_by_date(transactions_data, reverse)

    actual_dates = [item["date"].split("T")[0] for item in sorted_data]
    assert actual_dates == expected_order
