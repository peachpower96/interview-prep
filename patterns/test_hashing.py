import pytest

from hashing import (
    completed_per_user,
    first_unique,
    longest_consecutive_run,
    new_users_per_day,
    nth_missing,
    pair_for_target,
    top_k_categories,
)


@pytest.mark.parametrize("values,target,expected", [
    ([1800, 2400, 1250, 3175], 3050, [0, 2]),
    ([1000, 2000, 3000], 5000, [1, 2]),
    ([500, 500], 1000, [0, 1]),
    ([500, 300, 700], 1000, [1, 2]),     # 500 must not pair with itself
    ([-200, 700, 1500], 500, [0, 1]),
])
def test_pair_for_target(values, target, expected):
    assert pair_for_target(values, target) == expected


def test_new_users_per_day():
    events = [(101, "2026-10-01", "completed"), (102, "2026-10-01", "completed"),
              (101, "2026-10-01", "completed"), (103, "2026-10-02", "cancelled"),
              (101, "2026-10-02", "completed"), (104, "2026-10-02", "completed"),
              (103, "2026-10-03", "completed"), (102, "2026-10-03", "completed"),
              (104, "2026-10-03", "completed")]
    assert new_users_per_day(events) == {"2026-10-01": 2, "2026-10-02": 1, "2026-10-03": 1}


def test_new_users_per_day_unsorted_and_edge_cases():
    assert new_users_per_day([(1, "2026-10-05", "completed"), (1, "2026-10-03", "completed"),
                              (2, "2026-10-04", "cancelled")]) == {"2026-10-03": 1}
    assert new_users_per_day([(7, "2026-10-01", "cancelled")]) == {}
    assert new_users_per_day([]) == {}


def _recs(*pairs):
    return [{"category": c, "status": s} for c, s in pairs]


def test_top_k_categories():
    recs = _recs(("downtown", "completed"), ("airport", "completed"), ("downtown", "completed"),
                 ("harbour", "completed"), ("airport", "completed"), ("midtown", "completed"),
                 ("downtown", "completed"), ("airport", "completed"), ("harbour", "completed"),
                 ("midtown", "cancelled"), ("midtown", "cancelled"))
    assert top_k_categories(recs, 2) == ["airport", "downtown"]
    assert top_k_categories(recs, 3) == ["airport", "downtown", "harbour"]


def test_top_k_categories_edges():
    assert top_k_categories(_recs(("a", "cancelled"), ("a", "cancelled"), ("b", "completed")), 1) == ["b"]
    assert top_k_categories(_recs(("b", "completed"), ("a", "completed")), 5) == ["a", "b"]
    assert top_k_categories([], 3) == []
    assert top_k_categories(_recs(("a", "completed")), 0) == []


def test_completed_per_user():
    ev = [(11, "completed"), (11, "completed"), (12, "cancelled"), (12, "completed"), (13, "cancelled")]
    assert completed_per_user(ev) == {11: 2, 12: 1}
    assert completed_per_user([(5, "completed"), (5, "cancelled"), (5, "completed")]) == {5: 2}
    assert completed_per_user([(9, "cancelled")]) == {}
    assert completed_per_user([]) == {}


@pytest.mark.parametrize("nums,expected", [
    ([100, 4, 200, 1, 3, 2], 4),
    ([1, 2, 2, 3], 3),
    ([10, 5, 12, 3, 55, 30, 4, 11, 2], 4),
    ([5, 4, 3, 2, 1], 5),
    ([-1, 0, 1], 3),
    ([7], 1),
    ([], 0),
])
def test_longest_consecutive_run(nums, expected):
    assert longest_consecutive_run(nums) == expected


@pytest.mark.parametrize("nums,expected", [
    ([4, 5, 4, 6, 5], 6),
    ([9, 3, 9, 7, 3, 8], 7),
    ([1, 1, 2, 2], None),
    ([7], 7),
    ([], None),
    ([3, 3, 1, 2, 1, 2, 5], 5),
])
def test_first_unique(nums, expected):
    assert first_unique(nums) == expected


@pytest.mark.parametrize("ids,n,expected", [
    ([4, 7, 9, 10], 1, 5),
    ([4, 7, 9, 10], 2, 6),
    ([4, 7, 9, 10], 3, 8),
    ([4, 7, 9, 10], 4, 11),   # runs past the end
    ([5], 2, 7),
    ([1, 2, 3], 1, 4),
    ([2, 100], 50, 52),
])
def test_nth_missing(ids, n, expected):
    assert nth_missing(ids, n) == expected
