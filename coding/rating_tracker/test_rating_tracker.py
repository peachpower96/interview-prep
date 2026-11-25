from rating_tracker import RatingTracker


def make():
    return RatingTracker(
        ["kimchi", "miso", "sushi", "moussaka", "ramen", "bulgogi"],
        ["korean", "japanese", "japanese", "greek", "japanese", "korean"],
        [9, 12, 8, 15, 14, 7],
    )


def test_standard_example():
    t = make()
    assert t.highest_rated("korean") == "kimchi"
    assert t.highest_rated("japanese") == "ramen"
    t.change_rating("sushi", 16)
    assert t.highest_rated("japanese") == "sushi"
    t.change_rating("ramen", 16)
    assert t.highest_rated("japanese") == "ramen"   # tie: name sorts first


def test_tie_goes_to_earlier_name():
    t = RatingTracker(["b", "a", "c"], ["x", "x", "x"], [5, 5, 3])
    assert t.highest_rated("x") == "a"


def test_rating_can_go_down():
    t = make()
    t.change_rating("moussaka", 1)
    assert t.highest_rated("greek") == "moussaka"


def test_categories_stay_apart():
    t = make()
    t.change_rating("kimchi", 1)
    assert t.highest_rated("korean") == "bulgogi"
    assert t.highest_rated("greek") == "moussaka"


def test_remove_best_next_takes_over():
    t = make()
    t.remove_item("ramen")
    assert t.highest_rated("japanese") == "miso"
    t.remove_item("miso")
    assert t.highest_rated("japanese") == "sushi"


def test_remove_everything_in_category():
    t = make()
    t.remove_item("moussaka")
    assert t.highest_rated("greek") == ""


def test_change_then_remove():
    t = make()
    t.change_rating("sushi", 20)
    t.remove_item("sushi")
    assert t.highest_rated("japanese") == "ramen"


def test_remove_twice_is_safe():
    t = make()
    t.remove_item("ramen")
    t.remove_item("ramen")
    assert t.highest_rated("japanese") == "miso"
