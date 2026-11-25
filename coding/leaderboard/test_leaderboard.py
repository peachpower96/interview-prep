from leaderboard import Leaderboard


def make():
    b = Leaderboard()
    for pid, score in [(1, 73), (2, 56), (3, 39), (4, 51), (5, 4)]:
        b.add_score(pid, score)
    return b


def test_top():
    b = make()
    assert b.top(1) == 73
    assert b.top(3) == 180


def test_scores_accumulate_per_player():
    b = Leaderboard()
    b.add_score(1, 10)
    b.add_score(1, 5)
    b.add_score(2, 12)
    assert b.top(1) == 15
    assert b.top(2) == 27


def test_k_larger_than_players_and_empty_board():
    b = Leaderboard()
    assert b.top(3) == 0
    b.add_score(1, 10)
    b.add_score(2, 20)
    assert b.top(5) == 30


def test_reset_standard_example():
    b = make()
    assert b.top(1) == 73
    b.reset(1)
    b.reset(2)
    b.add_score(2, 51)
    assert b.top(3) == 141


def test_reset_then_add_starts_from_zero():
    b = Leaderboard()
    b.add_score(1, 50)
    b.reset(1)
    b.add_score(1, 7)
    assert b.top(1) == 7


def test_reset_unknown_player_is_safe():
    b = Leaderboard()
    b.reset(9)
    assert b.top(1) == 0
