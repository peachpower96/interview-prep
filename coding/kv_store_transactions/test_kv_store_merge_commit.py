from kv_store_merge_commit import KVStore


def test_commit_merges_inner_block_into_outer():
    s = KVStore()
    s.begin()
    s.set("a", "1")
    s.begin()
    s.set("a", "2")
    assert s.commit() is True
    assert s.get("a") == "2"
    assert s.rollback() is True      # outer block still open
    assert s.get("a") is None


def test_last_commit_makes_changes_permanent():
    s = KVStore()
    s.set("a", "0")
    s.begin()
    s.begin()
    s.set("a", "5")
    assert s.commit() is True
    assert s.commit() is True
    assert s.get("a") == "5"
    assert s.rollback() is False


def test_outer_rollback_undoes_inner_commit():
    s = KVStore()
    s.set("a", "0")
    s.begin()
    s.set("a", "1")
    s.begin()
    s.set("a", "2")
    s.commit()
    s.rollback()
    assert s.get("a") == "0"         # the older note won


def test_inner_commit_adds_notes_for_keys_outer_never_touched():
    s = KVStore()
    s.begin()
    s.set("a", "1")
    s.begin()
    s.set("b", "2")
    s.commit()
    s.rollback()
    assert s.get("a") is None and s.get("b") is None


def test_commit_with_no_block_open():
    assert KVStore().commit() is False
