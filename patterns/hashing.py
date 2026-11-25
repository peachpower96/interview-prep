"""Hash-map / set / counting patterns."""
import heapq
from collections import Counter


def pair_for_target(values, target):
    """Indices [i, j], i < j, of the two values that sum to target (exactly one pair exists).

    One pass with a dict value -> index. Check BEFORE storing, so a value cannot pair
    with itself. O(n) time, O(n) space (vs O(n^2) time for two loops).
    """
    seen = {}
    for i, v in enumerate(values):
        need = target - v
        if need in seen:
            return [seen[need], i]
        seen[v] = i
    return []


def new_users_per_day(events):
    """events: (user_id, 'YYYY-MM-DD', status). Return {day: number of users whose first
    completed event was that day}. Input is NOT sorted.

    Python twin of: WHERE status='completed' -> GROUP BY user, MIN(day) -> GROUP BY day, COUNT.
    ISO dates compare correctly as plain strings.
    """
    first = {}
    for user, day, status in events:
        if status != "completed":
            continue
        if user not in first or day < first[user]:
            first[user] = day
    return dict(Counter(first.values()))


def top_k_categories(records, k):
    """Top k categories by number of completed records; ties broken alphabetically.

    Counter + heapq.nsmallest with key (-count, name): O(c log k) instead of sorting all
    c categories. For data that does not fit in memory, stream it and keep only the Counter.
    """
    counts = Counter(r["category"] for r in records if r["status"] == "completed")
    best = heapq.nsmallest(k, counts.items(), key=lambda kv: (-kv[1], kv[0]))
    return [name for name, _ in best]


def completed_per_user(events):
    """events: (user_id, status). Count completed events per user (users with none omitted).

    Debugging drill: the buggy original assigned `= 1` instead of adding 1, and also counted
    non-completed events. Narrate: run it, compare to the expected output, trace one user.
    """
    counts = {}
    for user, status in events:
        if status == "completed":
            counts[user] = counts.get(user, 0) + 1
    return counts


def longest_consecutive_run(nums):
    """Length of the longest run of consecutive integers (unsorted, repeats allowed). O(n).

    Set lookups; only start counting at a number whose predecessor is NOT in the set.
    Without that check every run is recounted from every member (O(n^2) worst case).
    """
    s = set(nums)
    best = 0
    for n in s:
        if n - 1 in s:
            continue
        length = 1
        while n + length in s:
            length += 1
        best = max(best, length)
    return best


def first_unique(nums):
    """First number (by position) that appears exactly once, else None.

    Two passes: count, then scan the ORIGINAL list (not the counter's keys) for position.
    """
    counts = Counter(nums)
    for x in nums:
        if counts[x] == 1:
            return x
    return None


def nth_missing(ids, n):
    """ids: sorted unique ints (non-empty). The missing numbers are those greater than ids[0]
    that are not in the list; return the n-th (from 1), counting past the end if needed.

    Walk the gaps between neighbours: O(len(ids)), O(1) space. Follow-up: binary search on
    "missing before index i" = ids[i] - ids[0] - i, which only increases.
    """
    for i in range(1, len(ids)):
        gap = ids[i] - ids[i - 1] - 1
        if n <= gap:
            return ids[i - 1] + n
        n -= gap
    return ids[-1] + n
