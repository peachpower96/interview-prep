import pytest

from arrays_sorting import merge_sort, merge_sorted, product_except_self


@pytest.mark.parametrize("a,b,expected", [
    ([1, 4, 9], [2, 3, 10], [1, 2, 3, 4, 9, 10]),
    ([5], [1, 2, 3, 4], [1, 2, 3, 4, 5]),
    ([1, 3, 3], [3], [1, 3, 3, 3]),
    ([], [1, 2], [1, 2]),
    ([1, 2], [], [1, 2]),
    ([], [], []),
])
def test_merge_sorted(a, b, expected):
    assert merge_sorted(a, b) == expected


@pytest.mark.parametrize("items,expected", [
    ([5, 2, 9, 1, 5, 6], [1, 2, 5, 5, 6, 9]),
    ([3, 2, 1], [1, 2, 3]),
    ([1, 2, 3, 4], [1, 2, 3, 4]),
    ([0, -2, 7, -2], [-2, -2, 0, 7]),
    ([42], [42]),
    ([], []),
])
def test_merge_sort(items, expected):
    assert merge_sort(items) == expected


def test_merge_sort_does_not_mutate_input():
    xs = [3, 1, 2]
    merge_sort(xs)
    assert xs == [3, 1, 2]


@pytest.mark.parametrize("nums,expected", [
    ([1, 2, 3, 4], [24, 12, 8, 6]),
    ([2, 0, 5], [0, 10, 0]),
    ([0, 0, 3], [0, 0, 0]),
    ([-1, 2, -3], [-6, 3, -2]),
    ([5], [1]),
    ([], []),
])
def test_product_except_self(nums, expected):
    assert product_except_self(nums) == expected
