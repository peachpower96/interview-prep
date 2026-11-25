"""Stack and queue patterns."""
from collections import deque


def is_balanced(s):
    """True if every ( [ { is closed by the matching bracket in order; other characters ignored.

    List as a stack; dict of closing -> opening. Traps: closing with an empty stack, and
    leftover openings at the end (`return not stack`). O(n).
    """
    pairs = {")": "(", "]": "[", "}": "{"}
    stack = []
    for ch in s:
        if ch in "([{":
            stack.append(ch)
        elif ch in pairs:
            if not stack or stack.pop() != pairs[ch]:
                return False
    return not stack


def rolling_counts(times, window):
    """times sorted ascending (seconds). For each t, count items in (t - window, t].

    deque: new item joins the back, old ones leave from the front (popleft is O(1);
    list.pop(0) is O(n)). Each item enters and leaves once, so O(n) total.
    """
    recent = deque()
    counts = []
    for t in times:
        recent.append(t)
        while recent[0] <= t - window:   # fell out of the window
            recent.popleft()
        counts.append(len(recent))
    return counts


def surviving_collisions(items):
    """Signed ints on one lane: sign = direction (+ right, - left), abs = size.
    A right-mover meeting a left-mover: the smaller is removed, equal sizes both removed.
    Return survivors in order.

    Stack + `while` (not `if`): one big left-mover can remove several right-movers.
    Only a right-mover on top of the stack can meet a new left-mover. O(n).
    """
    stack = []
    for v in items:
        alive = True
        while alive and v < 0 and stack and stack[-1] > 0:
            if stack[-1] < -v:
                stack.pop()
            elif stack[-1] == -v:
                stack.pop()
                alive = False
            else:
                alive = False
        if alive:
            stack.append(v)
    return stack


class MinStack:
    """Stack with O(1) push, pop, top, get_min. Each entry stores (value, min so far),
    so popping restores the previous minimum automatically (no duplicate-min bug)."""

    def __init__(self):
        self.items = []

    def push(self, x):
        smallest = x if not self.items else min(x, self.items[-1][1])
        self.items.append((x, smallest))

    def pop(self):
        return self.items.pop()[0] if self.items else None

    def top(self):
        return self.items[-1][0] if self.items else None

    def get_min(self):
        return self.items[-1][1] if self.items else None
