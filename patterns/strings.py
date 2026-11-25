"""String patterns: sliding windows, runs, nested data, streaming."""
from collections import Counter


def longest_no_repeat(s):
    """Length of the longest substring with no repeated character. O(n).

    Window [start, i]; dict char -> last index. Only move start if the earlier copy is INSIDE
    the window (last_seen >= start), otherwise 'abba' moves start backwards.
    """
    last_seen = {}
    start = 0
    best = 0
    for i, ch in enumerate(s):
        if ch in last_seen and last_seen[ch] >= start:
            start = last_seen[ch] + 1
        last_seen[ch] = i
        best = max(best, i - start + 1)
    return best


def compress_runs(s):
    """Replace each run of the same character with char + count; omit the count when 1.
    'aaabcc' -> 'a3bc2'. Runs are consecutive (aabbaa -> a2b2a2), so not a Counter.

    Flush the last run after the loop; build with a list and ''.join. O(n).
    """
    if not s:
        return ""
    parts = []
    current, count = s[0], 1
    for ch in s[1:]:
        if ch == current:
            count += 1
        else:
            parts.append(current + (str(count) if count > 1 else ""))
            current, count = ch, 1
    parts.append(current + (str(count) if count > 1 else ""))
    return "".join(parts)


def min_window(s, t):
    """Shortest substring of s containing every character of t (with multiplicity, case
    sensitive). Ties: earliest start. None found: ''.

    Grow right until covered, shrink left while still covered. `missing` (total chars still
    needed) makes the "covers t" check O(1) instead of comparing two Counters each step.
    Record with strict < so ties keep the earlier start. O(len(s) + len(t)).
    """
    need = Counter(t)
    missing = len(t)
    left = 0
    best_len, best_start = float("inf"), 0
    for right, ch in enumerate(s):
        if need[ch] > 0:
            missing -= 1
        need[ch] -= 1
        while missing == 0:
            if right - left + 1 < best_len:
                best_len, best_start = right - left + 1, left
            need[s[left]] += 1
            if need[s[left]] > 0:
                missing += 1
            left += 1
    return "" if best_len == float("inf") else s[best_start:best_start + best_len]


def flatten(obj, prefix=""):
    """Flatten nested dicts, joining keys with '.'. Non-dict values (including lists) are kept
    whole; an empty nested dict contributes nothing. Recursion depth = nesting depth.
    Ask whether lists should be expanded (a.0, a.1)."""
    out = {}
    for key, value in obj.items():
        name = prefix + "." + key if prefix else key
        if isinstance(value, dict):
            out.update(flatten(value, name))
        else:
            out[name] = value
    return out


def kth_non_empty_line(lines, k):
    """k-th (from 1) non-empty line of any iterable of lines, without its line ending; whitespace-
    only lines count as empty. None if fewer than k (or k < 1).

    Stream: one line in memory at a time, stop as soon as found. Follow-up (last k lines):
    deque(maxlen=k).
    """
    count = 0
    for line in lines:
        text = line.rstrip("\r\n")
        if not text.strip():
            continue
        count += 1
        if count == k:
            return text
    return None
