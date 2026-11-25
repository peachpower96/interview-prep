from versioned_kv import VersionedKV


def test_versions_are_global_and_increase():
    s = VersionedKV()
    assert [s.set("a", "x"), s.set("b", "y"), s.set("a", "z"), s.set("c", "w")] == [1, 2, 3, 4]


def test_gaps_belong_to_other_keys():
    s = VersionedKV()
    s.set("a", "x")
    s.set("b", "y")
    s.set("b", "y2")
    s.set("a", "z")
    assert [s.get("a", v) for v in (1, 2, 3, 4)] == ["x", "x", "x", "z"]


def test_exact_version_counts():
    s = VersionedKV()
    s.set("a", "x")
    s.set("a", "z")
    assert s.get("a", 1) == "x"
    assert s.get("a", 2) == "z"


def test_before_first_write_is_none():
    s = VersionedKV()
    s.set("b", "y")
    s.set("a", "x")
    assert s.get("a", 1) is None
    assert s.get("a", 0) is None
    assert s.get("a", 2) == "x"


def test_unknown_key_is_none():
    s = VersionedKV()
    s.set("a", "x")
    assert s.get("zzz", 5) is None


def test_version_past_latest_returns_latest():
    s = VersionedKV()
    s.set("a", "x")
    s.set("a", "z")
    assert s.get("a", 100) == "z"


def test_many_writes_binary_search():
    s = VersionedKV()
    for i in range(50):
        s.set("k", i)
    assert s.get("k", 1) == 0
    assert s.get("k", 25) == 24
    assert s.get("k", 50) == 49
    assert s.get("k", 51) == 49


def test_interleaved_keys():
    s = VersionedKV()
    s.set("a", 1)
    s.set("b", 10)
    s.set("a", 2)
    s.set("b", 20)
    s.set("a", 3)
    assert [s.get("a", v) for v in range(7)] == [None, 1, 1, 2, 2, 3, 3]
    assert [s.get("b", v) for v in range(7)] == [None, None, 10, 10, 20, 20, 20]
