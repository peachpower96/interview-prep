from lfu_cache import LFUCache


def test_standard_example():
    c = LFUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == 1
    c.put(3, 3)           # evicts 2 (fewest uses)
    assert c.get(2) == -1
    assert c.get(3) == 3
    c.put(4, 4)           # 1 and 3 tie; evicts 1 (least recent)
    assert c.get(1) == -1
    assert c.get(3) == 3
    assert c.get(4) == 4


def test_tie_goes_to_least_recently_used():
    c = LFUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    c.put(3, 3)           # 1 and 2 tie at 1 use; evicts 1
    assert c.get(1) == -1
    assert c.get(2) == 2
    assert c.get(3) == 3


def test_put_existing_counts_as_use():
    c = LFUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    c.put(1, 10)
    c.put(3, 3)           # evicts 2
    assert c.get(2) == -1
    assert c.get(1) == 10
    assert c.get(3) == 3


def test_capacity_zero_stores_nothing():
    c = LFUCache(0)
    c.put(1, 1)
    assert c.get(1) == -1


def test_low_use_beats_recent_use():
    c = LFUCache(2)
    c.put(1, 1)
    c.get(1)
    c.put(2, 2)
    c.put(3, 3)           # evicts 2 (1 use) not 1 (2 uses)
    assert c.get(2) == -1
    assert c.get(1) == 1
    assert c.get(3) == 3
