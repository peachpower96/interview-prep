"""Time-based key-value store (LeetCode 981), with out-of-order writes.

Pattern: per key, two parallel sorted lists (timestamps, values) + binary search.
get is O(log n). set is O(n) worst case because inserting mid-list shifts items.
"""
from bisect import bisect_left, bisect_right


class TimeMap:
    def __init__(self):
        self.times = {}   # key -> sorted timestamps
        self.values = {}  # key -> values, same order

    def set(self, key, value, timestamp):
        times = self.times.setdefault(key, [])
        values = self.values.setdefault(key, [])
        i = bisect_left(times, timestamp)
        if i < len(times) and times[i] == timestamp:
            values[i] = value            # same timestamp again: overwrite
        else:
            times.insert(i, timestamp)   # keep both lists sorted
            values.insert(i, value)

    def get(self, key, timestamp):
        """Latest value set at or before `timestamp`, else ''."""
        times = self.times.get(key, [])
        i = bisect_right(times, timestamp) - 1
        if i < 0:
            return ""
        return self.values[key][i]
