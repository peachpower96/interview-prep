from rotting_oranges import minutes_to_rot


def test_standard_example():
    assert minutes_to_rot([[2, 1, 1], [1, 1, 0], [0, 1, 1]]) == 4


def test_unreachable_fresh_orange():
    assert minutes_to_rot([[2, 1, 1], [0, 1, 1], [1, 0, 1]]) == -1


def test_nothing_fresh():
    assert minutes_to_rot([[0, 2]]) == 0
    assert minutes_to_rot([[0]]) == 0


def test_fresh_with_no_rotten():
    assert minutes_to_rot([[1]]) == -1


def test_sources_spread_at_the_same_time():
    assert minutes_to_rot([[2, 1, 1, 2]]) == 1


def test_empty_cell_blocks_spread():
    assert minutes_to_rot([[2, 0, 1]]) == -1


def test_diagonal_does_not_count():
    assert minutes_to_rot([[2, 0], [0, 1]]) == -1


def test_input_not_mutated():
    grid = [[2, 1]]
    minutes_to_rot(grid)
    assert grid == [[2, 1]]
