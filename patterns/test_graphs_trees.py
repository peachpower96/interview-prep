import pytest

from graphs_trees import count_regions, is_valid_bst, shortest_route


@pytest.mark.parametrize("grid,start,goal,expected", [
    (["...", ".#.", "..."], (0, 0), (2, 2), 4),
    ([".#.", ".#.", ".#."], (0, 0), (0, 2), -1),
    (["..", ".."], (1, 1), (1, 1), 0),
    (["....", "###.", "....", ".###", "...."], (0, 0), (4, 3), 13),
    ([".....",], (0, 4), (0, 0), 4),
])
def test_shortest_route(grid, start, goal, expected):
    assert shortest_route(grid, start, goal) == expected


@pytest.mark.parametrize("grid,expected", [
    (["..#", "#.#", "#.."], 1),
    ([".#.", "#.#", ".#."], 5),          # diagonals do not connect
    (["###"], 0),
    ([], 0),
    (["...."], 1),
    (["..#..", "..#..", "#####", "....."], 3),
])
def test_count_regions(grid, expected):
    assert count_regions(grid) == expected


def leaf(v):
    return (v, None, None)


@pytest.mark.parametrize("tree,expected", [
    ((2, leaf(1), leaf(3)), True),
    ((5, leaf(1), (4, leaf(3), leaf(6))), False),
    ((5, leaf(4), (6, leaf(3), leaf(7))), False),    # deep value breaks root's rule
    (None, True),
    ((2, leaf(2), None), False),                     # duplicate
    ((0, leaf(-5), leaf(3)), True),                  # zero is a value, not "no value"
])
def test_is_valid_bst(tree, expected):
    assert is_valid_bst(tree) is expected
