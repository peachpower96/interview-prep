import pytest

from intervals_heaps import assign_workers, covered_length


@pytest.mark.parametrize("intervals,expected", [
    ([(0, 10), (5, 15), (20, 25)], 20),
    ([(0, 10), (10, 20)], 20),
    ([(0, 100), (10, 20)], 100),          # nested: end must use max()
    ([(20, 25), (0, 10), (5, 15)], 20),   # unsorted
    ([(3, 4)], 1),
    ([], 0),
])
def test_covered_length(intervals, expected):
    assert covered_length(intervals) == expected


@pytest.mark.parametrize("tasks,expected", [
    ([[60, 30], [70, 10], [90, 15], [60, 5]], [0, 1, 0, 1]),
    ([[0, 10], [10, 5], [10, 7]], [0, 0, 1]),               # touching reuses a worker
    ([[200, 10], [0, 100], [100, 50], [0, 30]], [0, 0, 0, 1]),
    ([], []),
    ([[0, 10]], [0]),
])
def test_assign_workers(tasks, expected):
    assert assign_workers(tasks) == expected


def test_assign_workers_does_not_mutate_input():
    tasks = [[5, 1], [0, 1]]
    assert assign_workers(tasks) == [0, 0]
    assert tasks == [[5, 1], [0, 1]]
