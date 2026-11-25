"""Read N characters given a chunked reader that is called repeatedly
(LeetCode 158, adapted to return a string).

Pattern: keep a leftover buffer on the object. Fetching more than you return
is normal; dropping the extras is the classic bug.
O(n) per call, O(1) extra space (leftover is at most chunk_size - 1 chars).
"""


class ChunkReader:
    """Stand-in for the provided low-level reader: up to 4 chars per call, '' at the end."""

    def __init__(self, text):
        self.text = text
        self.pos = 0

    def read4(self):
        chunk = self.text[self.pos:self.pos + 4]
        self.pos += 4
        return chunk


class BufferedReader:
    def __init__(self, reader):
        self.reader = reader
        self.leftover = ""   # fetched but not yet returned

    def read(self, n):
        out = self.leftover
        self.leftover = ""
        while len(out) < n:
            chunk = self.reader.read4()
            if chunk == "":
                break
            out += chunk
        self.leftover = out[n:]
        return out[:n]
