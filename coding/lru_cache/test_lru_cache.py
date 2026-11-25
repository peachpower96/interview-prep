from lru_cache import LRUCache


def test_standard_example():
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == 1
    c.put(3, 3)           # evicts 2
    assert c.get(2) == -1
    c.put(4, 4)           # evicts 1
    assert c.get(1) == -1
    assert c.get(3) == 3
    assert c.get(4) == 4


def test_put_existing_key_refreshes_it():
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    c.put(1, 10)
    c.put(3, 3)           # evicts 2, not 1
    assert c.get(1) == 10
    assert c.get(2) == -1


def test_get_refreshes_key():
    c = LRUCache(2)
    c.put(1, 1)
    c.put(2, 2)
    c.get(1)
    c.put(3, 3)           # evicts 2
    assert c.get(1) == 1
    assert c.get(2) == -1


def test_missing_key():
    assert LRUCache(2).get(5) == -1


def test_capacity_one():
    c = LRUCache(1)
    c.put(1, 1)
    c.put(2, 2)
    assert c.get(1) == -1
    assert c.get(2) == 2
