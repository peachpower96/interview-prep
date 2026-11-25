"""Globally versioned key-value store.

One version counter is shared by all keys; every set takes the next number.
get(key, version) returns the value from the key's latest write at or before
`version` (a predecessor lookup, not exact-match and not nearest-by-distance).

Pattern: per-key append-only history of (version, value), sorted by construction
because the store hands out the versions; binary search for the boundary.
set O(1), get O(log h) for a key with h writes, storage O(total writes).

Follow-up notes:
  * Simultaneous writers: one lock around "increment counter + append" so a
    reader never sees version 8 while 7 is still being written.
  * Retention cutoff: keep each key's last write at or before the cutoff plus
    every later one, or reads just after the cutoff will wrongly find nothing.
"""


class VersionedKV:
    def __init__(self):
        self.version = 0
        self.history = {}   # key -> [(version, value), ...] oldest first

    def set(self, key, value):
        self.version += 1
        self.history.setdefault(key, []).append((self.version, value))
        return self.version

    def get(self, key, version):
        pairs = self.history.get(key, [])
        low, high = 0, len(pairs) - 1
        best = None
        while low <= high:
            mid = (low + high) // 2
            if pairs[mid][0] <= version:
                best = pairs[mid][1]   # valid; a later one may also fit
                low = mid + 1
            else:
                high = mid - 1
        return best
