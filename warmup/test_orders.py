import pytest
from warmup.orders import average_amount, add_tag, get_page


# --- average_amount 테스트 ---

def test_average_amount_normal():
    """정상적인 금액 목록이 주어졌을 때 평균을 올바르게 계산하는지 검증."""
    amounts = [1000, 2000, 3000]
    assert average_amount(amounts) == 2000


def test_average_amount_empty_raises_zero_division():
    """빈 목록 전달 시 0으로 나누기 오류(ZeroDivisionError)가 발생하는지 감지."""
    with pytest.raises(ZeroDivisionError):
        average_amount([])


# --- add_tag 테스트 ---

def test_add_tag_basic():
    """주문 객체에 태그가 정상적으로 추가되는지 검증."""
    order = {"id": 1}
    result = add_tag(order, "new")
    assert result["tags"] == ["new"]


def test_add_tag_mutable_default_argument_bug():
    """
    기본 인자 tags=[]가 호출 간 공유되는 가변 기본 인자 버그 감지.
    독립된 두 호출 시 태그 목록이 누적되지 않아야 한다.
    """
    order1 = {"id": 1}
    order2 = {"id": 2}

    add_tag(order1, "tag1")
    add_tag(order2, "tag2")

    # order2는 'tag1'이 누적되지 않고 ['tag2']만 가지고 있어야 함
    assert order2["tags"] == ["tag2"]
    assert order1["tags"] is not order2["tags"]


# --- get_page 테스트 ---

@pytest.mark.parametrize(
    ("page", "size", "expected"),
    [
        (1, 10, list(range(0, 10))),     # 1페이지는 0~9번 항목이어야 함 (현재 버그: 10~19 반환)
        (2, 10, list(range(10, 20))),    # 2페이지는 10~19번 항목이어야 함
        (3, 10, [20, 21, 22]),           # 마지막 부분 페이지
    ],
)
def test_get_page_pagination(page, size, expected):
    """1-based 페이지네이션이 의도대로 동작하는지 검증 (1페이지 오프셋 버그 감지)."""
    orders = list(range(23))
    assert get_page(orders, page=page, size=size) == expected


def test_get_page_default_size():
    """기본 size=10을 적용하여 1페이지를 요청했을 때 첫 10개 항목이 반환되는지 검증."""
    orders = list(range(15))
    assert get_page(orders, page=1) == list(range(10))
