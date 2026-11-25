from time_map import TimeMap


def test_basic_example():
    t = TimeMap()
    t.set("foo", "bar", 1)
    assert t.get("foo", 1) == "bar"
    assert t.get("foo", 3) == "bar"
    t.set("foo", "bar2", 4)
    assert t.get("foo", 4) == "bar2"
    assert t.get("foo", 5) == "bar2"


def test_before_first_entry_and_missing_key():
    t = TimeMap()
    t.set("a", "x", 10)
    assert t.get("a", 5) == ""
    assert t.get("nope", 5) == ""


def test_between_entries():
    t = TimeMap()
    t.set("a", "x", 10)
    t.set("a", "y", 20)
    assert t.get("a", 15) == "x"
    assert t.get("a", 19) == "x"
    assert t.get("a", 20) == "y"
    assert t.get("a", 99) == "y"


def test_keys_are_independent():
    t = TimeMap()
    t.set("a", "x", 1)
    t.set("b", "y", 2)
    assert t.get("a", 5) == "x"
    assert t.get("b", 5) == "y"
    assert t.get("b", 1) == ""


def test_out_of_order_writes():
    t = TimeMap()
    t.set("a", "late", 20)
    t.set("a", "early", 10)
    assert t.get("a", 15) == "early"
    assert t.get("a", 25) == "late"
    assert t.get("a", 5) == ""


def test_insert_in_middle():
    t = TimeMap()
    t.set("a", "x", 10)
    t.set("a", "z", 30)
    t.set("a", "y", 20)
    assert t.get("a", 25) == "y"
    assert t.get("a", 30) == "z"
    assert t.get("a", 10) == "x"


def test_same_timestamp_overwrites():
    t = TimeMap()
    t.set("a", "x", 10)
    t.set("a", "y", 10)
    assert t.get("a", 10) == "y"
    assert t.get("a", 11) == "y"
