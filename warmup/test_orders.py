from warmup.orders import get_page


def test_get_page_first_page_starts_at_beginning():
    orders = list(range(1, 6))

    assert get_page(orders, page=1, size=2) == [1, 2]


def test_get_page_returns_requested_page():
    orders = list(range(1, 7))

    assert get_page(orders, page=2, size=2) == [3, 4]


def test_get_page_returns_partial_last_page():
    orders = list(range(1, 6))

    assert get_page(orders, page=3, size=2) == [5]


def test_get_page_out_of_range_returns_empty_list():
    orders = list(range(1, 6))

    assert get_page(orders, page=4, size=2) == []