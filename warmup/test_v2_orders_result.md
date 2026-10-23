# test_v2_orders 테스트 실행 결과 및 버그 분석 보고서

- **대상 파일**: [`warmup/orders.py`](file:///C:/workspaces/review-thermo/warmup/orders.py)
- **테스트 파일**: [`warmup/test_v2_orders.py`](file:///C:/workspaces/review-thermo/warmup/test_v2_orders.py)
- **실행 명령**: `pytest -v warmup/test_v2_orders.py`
- **테스트 결과 요약**: **1 PASSED / 5 FAILED** (의도된 버그 탐지 성공)

---

## 1. 테스트 실행 실제 로그 (Terminal Output)

```text
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.1.1, pluggy-1.7.0 -- C:\workspaces\review-thermo\.venv\Scripts\python.exe
cachedir: .pytest_cache
rootdir: C:\workspaces\review-thermo
configfile: pyproject.toml
plugins: anyio-4.15.1
collecting ... collected 6 items

warmup/test_v2_orders.py::test_average_amount_normal PASSED              [ 16%]
warmup/test_v2_orders.py::test_average_amount_empty_list FAILED          [ 33%]
warmup/test_v2_orders.py::test_add_tag_single_call FAILED                [ 50%]
warmup/test_v2_orders.py::test_add_tag_mutable_default_argument_bug FAILED [ 66%]
warmup/test_v2_orders.py::test_get_page_page_1_starts_at_first_item FAILED [ 83%]
warmup/test_v2_orders.py::test_get_page_page_2 FAILED                    [100%]

================================== FAILURES ===================================
_______________________ test_average_amount_empty_list ________________________

    def test_average_amount_empty_list():
        """빈 리스트가 들어왔을 때의 기대 동작.
    
        현재 orders.py는 ZeroDivisionError가 발생하므로,
        정상적인 기대(예: 0을 반환)를 작성하면 버그가 드러나며 실패(Red)합니다.
        """
>       assert average_amount([]) == 0
               ^^^^^^^^^^^^^^^^^^

warmup\test_v2_orders.py:21: 
_ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ _

amounts = []

    def average_amount(amounts):
        """주문 금액의 평균을 구한다."""
        total = sum(amounts)  # 금액을 모두 더한다
>       return total / len(amounts)  # 개수로 나눈다
               ^^^^^^^^^^^^^^^^^^^^
E       ZeroDivisionError: division by zero

warmup\orders.py:7: ZeroDivisionError
__________________________ test_add_tag_single_call ___________________________

    def test_add_tag_single_call():
        """단일 호출 시 정상적으로 태그가 추가된다."""
        order = {"id": 1}
        result = add_tag(order, "급송")
>       assert result["tags"] == ["급송"]
E       AssertionError: assert ['현대아파트1동1호', '급송'] == ['급송']
E         
E         At index 0 diff: '현대아파트1동1호' != '급송'
E         Left contains one more item: '급송'
E         
E         Full diff:
E           [
E         +     '현대아파트1동1호',
E               '급송',
E           ]

warmup\test_v2_orders.py:32: AssertionError
__________________ test_add_tag_mutable_default_argument_bug __________________

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
>       assert result2["tags"] == ["선물포장"]
E       AssertionError: assert ['현대아파트1동1호', '급송', '급송', '선물포장'] == ['선물포장']
E         
E         At index 0 diff: '현대아파트1동1호' != '선물포장'
E         Left contains 3 more items, first extra item: '급송'
E         
E         Full diff:
E           [
E         +     '현대아파트1동1호',
E         +     '급송',
E         +     '급송',
E               '선물포장',
E           ]

warmup\test_v2_orders.py:49: AssertionError
__________________ test_get_page_page_1_starts_at_first_item __________________

    def test_get_page_page_1_starts_at_first_item():
        """1페이지(page=1) 요청 시 목록의 첫 번째 요소부터 반환해야 한다.
    
        현재 orders.py는 start = page * size (즉, 1 * 2 = 2)부터 슬라이싱하여
        0번째, 1번째 아이템이 건너뛰어지는 버그가 있어 실패(Red)합니다.
        """
        orders = ["order_1", "order_2", "order_3", "order_4"]
        # 1페이지(사이즈 2)면 ["order_1", "order_2"]가 반환되어야 함
>       assert get_page(orders, page=1, size=2) == ["order_1", "order_2"]
E       AssertionError: assert ['order_3', 'order_4'] == ['order_1', 'order_2']
E         
E         At index 0 diff: 'order_3' != 'order_1'
E         
E         Full diff:
E           [
E         -     'order_1',
E         -     'order_2',
E         +     'order_3',
E         +     'order_4',
E           ]

warmup\test_v2_orders.py:64: AssertionError
____________________________ test_get_page_page_2 _____________________________

    def test_get_page_page_2():
        """2페이지(page=2) 요청 시 두 번째 페이지 범위를 반환해야 한다."""
        orders = ["order_1", "order_2", "order_3", "order_4"]
        # 2페이지(사이즈 2)면 ["order_3", "order_4"]가 반환되어야 함
>       assert get_page(orders, page=2, size=2) == ["order_3", "order_4"]
E       AssertionError: assert [] == ['order_3', 'order_4']
E         
E         Right contains 2 more items, first extra item: 'order_3'
E         
E         Full diff:
E         + []
E         - [
E         -     'order_3',
E         -     'order_4',
E         - ]

warmup\test_v2_orders.py:71: AssertionError
=========================== short test summary info ===========================
FAILED warmup/test_v2_orders.py::test_average_amount_empty_list - ZeroDivisionError: division by zero
FAILED warmup/test_v2_orders.py::test_add_tag_single_call - AssertionError: assert ['현대아파트1동1호', '급송'] == ['급송']
FAILED warmup/test_v2_orders.py::test_add_tag_mutable_default_argument_bug - AssertionError: assert ['현대아파트1동1호', '급송', '급송', '선물포장'] == ['선물포장']
FAILED warmup/test_v2_orders.py::test_get_page_page_1_starts_at_first_item - AssertionError: assert ['order_3', 'order_4'] == ['order_1', 'order_2']
FAILED warmup/test_v2_orders.py::test_get_page_page_2 - AssertionError: assert [] == ['order_3', 'order_4']
========================= 5 failed, 1 passed in 0.08s =========================
```

---

## 2. 테스트 결과 상세 분석 (드러난 버그 목록)

### 1) `average_amount(amounts)`
- **테스트 케이스**: [`test_average_amount_empty_list`](file:///C:/workspaces/review-thermo/warmup/test_v2_orders.py#L14-L21)
- **결과**: `ZeroDivisionError: division by zero`
- **원인 분석**:
  - `amounts`가 빈 리스트(`[]`)일 때 `len(amounts)`가 0이 되어 나누기 연산 시 예외가 발생합니다.
  - 리스트가 비어 있는 경우 `if not amounts: return 0` 등의 방어 로직이 필요합니다.

---

### 2) `add_tag(order, tag, tags=[])`
- **테스트 케이스**: [`test_add_tag_single_call`](file:///C:/workspaces/review-thermo/warmup/test_v2_orders.py#L27-L32), [`test_add_tag_mutable_default_argument_bug`](file:///C:/workspaces/review-thermo/warmup/test_v2_orders.py#L35-L49)
- **결과**:
  - `AssertionError: assert ['현대아파트1동1호', '급송'] == ['급송']`
  - `AssertionError: assert ['현대아파트1동1호', '급송', '급송', '선물포장'] == ['선물포장']`
- **원인 분석**:
  1. **파이썬 가변 기본 인자 버그**: 파이썬 함수 정의 시점의 기본 리스트(`tags=[]`)가 모듈 로드 시 메모리에 한 번만 생성되어 모든 호출 간에 공유됩니다.
  2. `orders.py` 모듈 하단의 실행 코드(`print(add_tag(..., "현대아파트1동1호"))`)로 인해 모듈 import 시점에 이미 기본 리스트에 `'현대아파트1동1호'`가 들어가 오염되어 있었습니다.
  3. 해결을 위해서는 `def add_tag(order, tag, tags=None): if tags is None: tags = []` 패턴을 적용해야 합니다.

---

### 3) `get_page(orders, page, size=10)`
- **테스트 케이스**: [`test_get_page_page_1_starts_at_first_item`](file:///C:/workspaces/review-thermo/warmup/test_v2_orders.py#L55-L64), [`test_get_page_page_2`](file:///C:/workspaces/review-thermo/warmup/test_v2_orders.py#L67-L71)
- **결과**:
  - 1페이지 요청 시: `['order_3', 'order_4'] == ['order_1', 'order_2']` 실패 (첫 2개 항목 누락)
  - 2페이지 요청 시: `[] == ['order_3', 'order_4']` 실패 (빈 리스트 반환)
- **원인 분석**:
  - `page`는 1부터 시작하는 1-based 페이지 번호이나 계산식이 `start = page * size`로 되어 있어, `page=1`일 때 `start=2`가 되어 0번~1번 항목이 스킵됩니다.
  - 올바른 공식은 `start = (page - 1) * size` 입니다.
