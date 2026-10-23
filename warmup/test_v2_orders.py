import pytest
from warmup.orders import average_amount, add_tag, get_page


# ==========================================
# 1. average_amount 테스트
# ==========================================

def test_average_amount_normal():
    """정상적인 금액 리스트의 평균을 계산한다."""
    amounts = [1000, 2000, 3000]
    assert average_amount(amounts) == 2000


def test_average_amount_empty_list():
    """빈 리스트가 들어왔을 때의 기대 동작.
    
    현재 orders.py는 ZeroDivisionError가 발생하므로,
    정상적인 기대(예: 0을 반환)를 작성하면 버그가 드러나며 실패(Red)합니다.
    """
    assert average_amount([]) == 0


# ==========================================
# 2. add_tag 테스트
# ==========================================

def test_add_tag_single_call():
    """단일 호출 시 정상적으로 태그가 추가된다."""
    order = {"id": 1}
    result = add_tag(order, "급송")
    assert result["tags"] == ["급송"]


def test_add_tag_mutable_default_argument_bug():
    """기본 인자 가변 객체(tags=[]) 버그 검증.
    
    서로 다른 주문에 대해 tags 인자 없이 순차 호출했을 때,
    앞서 추가된 태그가 다음 호출에 공유/누적되지 않고 독립적이어야 합니다.
    현재 orders.py는 기본 리스트를 공유하여 두 번째 호출 결과에 '급송'까지 포함되어 실패(Red)합니다.
    """
    order1 = {"id": 1}
    add_tag(order1, "급송")

    order2 = {"id": 2}
    result2 = add_tag(order2, "선물포장")

    # 기대: order2에는 ["선물포장"]만 있어야 함
    assert result2["tags"] == ["선물포장"]


# ==========================================
# 3. get_page 테스트
# ==========================================

def test_get_page_page_1_starts_at_first_item():
    """1페이지(page=1) 요청 시 목록의 첫 번째 요소부터 반환해야 한다.
    
    현재 orders.py는 start = page * size (즉, 1 * 2 = 2)부터 슬라이싱하여
    0번째, 1번째 아이템이 건너뛰어지는 버그가 있어 실패(Red)합니다.
    """
    orders = ["order_1", "order_2", "order_3", "order_4"]
    # 1페이지(사이즈 2)면 ["order_1", "order_2"]가 반환되어야 함
    assert get_page(orders, page=1, size=2) == ["order_1", "order_2"]


def test_get_page_page_2():
    """2페이지(page=2) 요청 시 두 번째 페이지 범위를 반환해야 한다."""
    orders = ["order_1", "order_2", "order_3", "order_4"]
    # 2페이지(사이즈 2)면 ["order_3", "order_4"]가 반환되어야 함
    assert get_page(orders, page=2, size=2) == ["order_3", "order_4"]
