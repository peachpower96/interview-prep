"""In-memory key-value store with nested transactions and an O(1) count.

Pattern: one live dict + a stack of undo logs + a value -> count index.
Every write goes through _put, so the index cannot drift from the data.
"""


class KVStore:
    def __init__(self):
        self.data = {}
        self.counts = {}  # value -> number of keys holding it
        self.logs = []    # one dict per open block: key -> (was_present, old_value)

    def _put(self, key, present, value):
        """The only place that changes self.data (keeps counts in sync)."""
        if key in self.data:
            old = self.data.pop(key)
            self.counts[old] -= 1
            if self.counts[old] == 0:
                del self.counts[old]
        if present:
            self.data[key] = value
            self.counts[value] = self.counts.get(value, 0) + 1

    def _remember(self, key):
        """Save the pre-block state of a key, once per block."""
        if self.logs and key not in self.logs[-1]:
            self.logs[-1][key] = (key in self.data, self.data.get(key))

    def set(self, key, value):
        self._remember(key)
        self._put(key, True, value)

    def get(self, key):
        return self.data.get(key)

    def unset(self, key):
        self._remember(key)
        self._put(key, False, None)

    def count(self, value):
        return self.counts.get(value, 0)

    def begin(self):
        self.logs.append({})

    def rollback(self):
        """Undo the innermost open block. False if none is open."""
        if not self.logs:
            return False
        for key, (present, old) in self.logs.pop().items():
            self._put(key, present, old)
        return True

    def commit(self):
        """Make all changes permanent and close every open block."""
        if not self.logs:
            return False
        self.logs.clear()
        return True
