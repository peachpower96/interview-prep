"""Fetch the next N items from a paginated source, keeping leftovers between calls.

Two variants of the same pattern:
  * WordFetcher     - pages addressed by number: fetch_page(i) -> (words, has_more)
  * StatefulFetcher - pages linked by tokens:   fetch(token) -> {"items": [...], "nextPage": token | None}

State that must survive between calls: where the next page is, the buffer of
items fetched but not yet returned, and whether the source has ended.
Only call the source when the buffer is not enough; never skip or repeat a page.
Use a deque so handing out items is O(1) each.
"""
from collections import deque


class WordFetcher:
    def __init__(self, fetch_page):
        self.fetch_page = fetch_page
        self.next_page = 0
        self.buffer = deque()
        self.has_more = True

    def fetch(self, n):
        while len(self.buffer) < n and self.has_more:
            words, self.has_more = self.fetch_page(self.next_page)
            self.next_page += 1
            self.buffer.extend(words)
        out = []
        while self.buffer and len(out) < n:
            out.append(self.buffer.popleft())
        return out


class StatefulFetcher:
    def __init__(self, fetch, first_token):
        self.fetch = fetch
        self.token = first_token    # next page to ask for; None once the source has ended
        self.buffer = deque()
        self.seen = set()           # tokens already read, to catch a pagination loop

    def fetch_n(self, n):
        if n <= 0:
            return []
        while len(self.buffer) < n and self.token is not None:
            if self.token in self.seen:
                raise ValueError("pagination loop: token repeated")
            page = self.fetch(self.token)   # if this raises, no state has changed yet
            self.seen.add(self.token)       # commit point: the page counts only now
            self.buffer.extend(page["items"])
            self.token = page.get("nextPage")
        out = []
        while self.buffer and len(out) < n:
            out.append(self.buffer.popleft())
        return out
