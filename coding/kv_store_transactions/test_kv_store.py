from kv_store import KVStore


def test_set_get_unset():
    s = KVStore()
    s.set("a", "1")
    assert s.get("a") == "1"
    assert s.get("b") is None
    s.set("a", "2")
    assert s.get("a") == "2"
    s.unset("a")
    assert s.get("a") is None
    s.unset("missing")  # must not raise


def test_rollback_one_block():
    s = KVStore()
    s.set("a", "1")
    s.begin()
    s.set("a", "2")
    assert s.get("a") == "2"
    assert s.rollback() is True
    assert s.get("a") == "1"


def test_nested_rollbacks():
    s = KVStore()
    s.begin()
    s.set("a", "1")
    s.begin()
    s.set("a", "2")
    s.set("b", "9")
    assert s.rollback() is True
    assert s.get("a") == "1" and s.get("b") is None
    assert s.rollback() is True
    assert s.get("a") is None


def test_commit_closes_every_block():
    s = KVStore()
    s.begin()
    s.set("a", "1")
    s.begin()
    s.set("a", "2")
    assert s.commit() is True
    assert s.rollback() is False
    assert s.get("a") == "2"


def test_set_twice_in_one_block_rolls_back_to_original():
    s = KVStore()
    s.set("a", "1")
    s.begin()
    s.set("a", "2")
    s.set("a", "3")
    s.rollback()
    assert s.get("a") == "1"


def test_unset_then_rollback_restores():
    s = KVStore()
    s.set("a", "1")
    s.begin()
    s.unset("a")
    assert s.get("a") is None
    s.rollback()
    assert s.get("a") == "1"


def test_no_block_open():
    s = KVStore()
    assert s.rollback() is False
    assert s.commit() is False


def test_count():
    s = KVStore()
    s.set("a", "x")
    s.set("b", "x")
    assert s.count("x") == 2
    s.set("a", "y")
    assert s.count("x") == 1 and s.count("y") == 1
    s.unset("b")
    assert s.count("x") == 0
    assert s.count("never") == 0


def test_count_through_rollback_and_commit():
    s = KVStore()
    s.set("a", "x")
    s.set("b", "x")
    s.begin()
    s.set("a", "y")
    s.unset("b")
    assert s.count("x") == 0 and s.count("y") == 1
    s.rollback()
    assert s.count("x") == 2 and s.count("y") == 0

    s2 = KVStore()
    s2.begin()
    s2.set("a", "x")
    s2.begin()
    s2.set("b", "x")
    s2.commit()
    assert s2.count("x") == 2
    assert s2.rollback() is False
    assert s2.count("x") == 2


def test_same_value_set_twice_counts_once():
    s = KVStore()
    s.set("a", "x")
    s.set("a", "x")
    assert s.count("x") == 1
