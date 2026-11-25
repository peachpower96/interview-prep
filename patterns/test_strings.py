import pytest

from strings import compress_runs, flatten, kth_non_empty_line, longest_no_repeat, min_window


@pytest.mark.parametrize("s,expected", [
    ("abcabcbb", 3), ("bbbbb", 1), ("pwwkew", 3), ("abba", 2), ("dvdf", 3), ("", 0), ("x", 1),
])
def test_longest_no_repeat(s, expected):
    assert longest_no_repeat(s) == expected


@pytest.mark.parametrize("s,expected", [
    ("aaabcc", "a3bc2"),
    ("abc", "abc"),
    ("aabbaa", "a2b2a2"),
    ("a" * 12, "a12"),
    ("a", "a"),
    ("", ""),
])
def test_compress_runs(s, expected):
    assert compress_runs(s) == expected


@pytest.mark.parametrize("s,t,expected", [
    ("AXXBXCXXAB", "ABC", "CXXAB"),
    ("AABXBAA", "AAB", "AAB"),          # tie: earliest
    ("abBA", "AAb", ""),                # case sensitive
    ("ADOBECODEBANC", "ABC", "BANC"),
    ("a", "aa", ""),
    ("ab", "ba", "ab"),
    ("a", "a", "a"),
])
def test_min_window(s, t, expected):
    assert min_window(s, t) == expected


def test_flatten():
    event = {"ride": {"id": 7, "driver": {"name": "Maya", "rating": 4.9}}, "city": "Toronto"}
    assert flatten(event) == {"ride.id": 7, "ride.driver.name": "Maya",
                              "ride.driver.rating": 4.9, "city": "Toronto"}
    assert flatten({"a": 1, "b": 2}) == {"a": 1, "b": 2}
    assert flatten({"a": {"b": {"c": 1}}}) == {"a.b.c": 1}
    assert flatten({"a": {"tags": [1, 2]}}) == {"a.tags": [1, 2]}
    assert flatten({"a": {}}) == {}
    assert flatten({}) == {}


def test_kth_non_empty_line():
    lines = ["a\n", "\n", "b\n", "   \n", "c"]
    assert kth_non_empty_line(iter(lines), 2) == "b"
    assert kth_non_empty_line(iter(lines), 3) == "c"
    assert kth_non_empty_line(iter(["a\n", "\n"]), 2) is None
    assert kth_non_empty_line(iter(["\r\n", "x\r\n"]), 1) == "x"
    assert kth_non_empty_line((s for s in ["\n", "only\n"]), 1) == "only"
    assert kth_non_empty_line(iter(["a\n"]), 0) is None
