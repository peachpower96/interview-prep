"""LRU cache (LeetCode 146). get and put are O(1).

Pattern: OrderedDict, oldest first / newest last. move_to_end on every use,
popitem(last=False) to evict. Without OrderedDict: dict + doubly linked list.
"""
from collections import OrderedDict


class LRUCache:
    def __init__(self, capacity):
        self.capacity = capacity
        self.items = OrderedDict()

    def get(self, key):
        if key not in self.items:
            return -1
        self.items.move_to_end(key)
        return self.items[key]

    def put(self, key, value):
        if key in self.items:
            self.items.move_to_end(key)
        self.items[key] = value
        if len(self.items) > self.capacity:
            self.items.popitem(last=False)
