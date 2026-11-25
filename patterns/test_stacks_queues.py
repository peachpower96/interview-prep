import pytest

from stacks_queues import MinStack, is_balanced, rolling_counts, surviving_collisions


@pytest.mark.parametrize("s,expected", [
    ('{"a": [1, 2]}', True),
    ('{"a": [1, 2}]', False),
    ("", True),
    ("((", False),
    ("))", False),
    ("a(b[c]{d}e)f", True),
    ("}", False),
])
def test_is_balanced(s, expected):
    assert is_balanced(s) is expected


@pytest.mark.parametrize("times,window,expected", [
    ([1, 2, 3, 301, 302], 300, [1, 2, 3, 3, 3]),
    ([0, 300, 600], 300, [1, 1, 1]),      # window excludes its start
    ([5, 5, 5], 10, [1, 2, 3]),
    ([], 60, []),
])
def test_rolling_counts(times, window, expected):
    assert rolling_counts(times, window) == expected


@pytest.mark.parametrize("items,expected", [
    ([5, 10, -5], [5, 10]),
    ([8, -8], []),
    ([10, 2, -5], [10]),                   # one item removes several
    ([-2, -1, 1, 2], [-2, -1, 1, 2]),      # moving apart never meet
    ([-5, 3], [-5, 3]),
    ([1, -2, -2, -2], [-2, -2, -2]),
    ([], []),
])
def test_surviving_collisions(items, expected):
    assert surviving_collisions(items) == expected


def test_min_stack_basic():
    s = MinStack()
    s.push(5)
    s.push(2)
    s.push(7)
    assert s.get_min() == 2
    assert s.pop() == 7
    assert s.get_min() == 2
    assert s.pop() == 2
    assert s.get_min() == 5
    assert s.top() == 5


def test_min_stack_duplicate_minimum_and_empty():
    s = MinStack()
    s.push(3)
    s.push(3)
    assert s.pop() == 3
    assert s.get_min() == 3
    e = MinStack()
    assert (e.pop(), e.top(), e.get_min()) == (None, None, None)


def test_min_stack_instances_do_not_share_state():
    a, b = MinStack(), MinStack()
    a.push(1)
    assert b.get_min() is None
