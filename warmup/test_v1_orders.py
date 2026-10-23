from warmup.orders import add_tag, average_amount, get_page


def test_average_amount_returns_mean():
    assert average_amount([10, 20, 30]) == 20


def test_add_tag_adds_tag_to_given_list():
    order = {"order": "주문1번", "tags": []}

    result = add_tag(order, "배송", tags=[])

    assert result == {"order": "주문1번", "tags": ["배송"]}


def test_add_tag_does_not_mutate_previous_order_tags():
    first_order = add_tag({"order": "주문1번"}, "첫 번째")
    first_tags = first_order["tags"].copy()
    second_order = add_tag({"order": "주문2번"}, "두 번째")

    assert first_order["tags"] == first_tags
    assert second_order["tags"] is not first_order["tags"]


def test_get_page_first_page_starts_at_beginning():
    assert get_page([1, 2, 3, 4, 5], page=1, size=2) == [1, 2]


def test_get_page_returns_second_page():
    assert get_page([1, 2, 3, 4, 5], page=2, size=2) == [3, 4]


def test_get_page_returns_partial_last_page():
    assert get_page([1, 2, 3, 4, 5], page=3, size=2) == [5]