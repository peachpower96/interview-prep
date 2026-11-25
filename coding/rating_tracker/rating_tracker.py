"""Highest-rated item per category (LeetCode 2353), plus item removal.

Pattern: one heap per category + lazy deletion. A heap cannot edit its middle,
so on a rating change push a NEW entry and leave the old one. When reading the
top, discard entries that no longer match the item's current rating.
highest_rated is O(log n) amortized; each stale entry is pushed/popped once.
Tie-break: highest rating, then the name that sorts first (heap key (-rating, name)).
"""
import heapq


class RatingTracker:
    def __init__(self, items, categories, ratings):
        self.rating = {}      # item -> current rating (absent = removed)
        self.category = {}    # item -> category
        self.heaps = {}       # category -> heap of (-rating, item), may hold stale entries
        for item, category, rating in zip(items, categories, ratings):
            self.rating[item] = rating
            self.category[item] = category
            self.heaps.setdefault(category, []).append((-rating, item))
        for heap in self.heaps.values():
            heapq.heapify(heap)

    def change_rating(self, item, new_rating):
        self.rating[item] = new_rating
        heapq.heappush(self.heaps[self.category[item]], (-new_rating, item))

    def remove_item(self, item):
        self.rating.pop(item, None)   # all its heap entries now go stale

    def highest_rated(self, category):
        """Best item in the category, or '' if none left."""
        heap = self.heaps.get(category, [])
        while heap:
            neg, item = heap[0]
            if self.rating.get(item) == -neg:   # still current
                return item
            heapq.heappop(heap)                 # stale: discard
        return ""
