"""Variant of the transactional KV store where commit() merges only the
innermost block into the block outside it (instead of closing every block).

If it was the outermost block, the changes become permanent. An outer rollback
still undoes merged changes. When merging undo logs, the OUTER (older) note wins
for a key, because an outer rollback must return to before the outer block began.
Ask which commit meaning is wanted before coding; say the choice out loud.
"""


class KVStore:
    def __init__(self):
        self.data = {}
        self.logs = []   # one dict per open block: key -> (was_present, old_value)

    def _remember(self, key):
        if self.logs and key not in self.logs[-1]:
            self.logs[-1][key] = (key in self.data, self.data.get(key))

    def set(self, key, value):
        self._remember(key)
        self.data[key] = value

    def get(self, key):
        return self.data.get(key)

    def unset(self, key):
        self._remember(key)
        self.data.pop(key, None)

    def begin(self):
        self.logs.append({})

    def rollback(self):
        if not self.logs:
            return False
        for key, (present, old) in self.logs.pop().items():
            if present:
                self.data[key] = old
            else:
                self.data.pop(key, None)
        return True

    def commit(self):
        if not self.logs:
            return False
        top = self.logs.pop()
        if self.logs:
            for key, saved in top.items():
                self.logs[-1].setdefault(key, saved)   # older note wins
        return True
