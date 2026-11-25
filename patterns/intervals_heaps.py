"""Interval sweeps and heap-based scheduling."""
import heapq


def covered_length(intervals):
    """Total length covered by at least one (start, end) interval; overlaps counted once.

    Sort by start, sweep keeping one current block. Extend with max(end, ...) (a short
    interval inside a long one must not shrink the block); add the last block after the loop.
    O(n log n).
    """
    total = 0
    cur_start = cur_end = None
    for start, end in sorted(intervals):
        if cur_end is None or start > cur_end:
            if cur_end is not None:
                total += cur_end - cur_start
            cur_start, cur_end = start, end
        else:
            cur_end = max(cur_end, end)
    if cur_end is not None:
        total += cur_end - cur_start
    return total


def assign_workers(tasks):
    """tasks: [start, duration]. Process by (start, input index). A worker is free again at
    start + duration (finishing exactly at a task's start is free). Give each task the
    smallest-ID free worker, else hire a new one (next ID from 0). Return worker IDs in the
    ORIGINAL input order; do not mutate the input.

    Two heaps: busy = (end_time, id), free = ids. Release finished workers before each task.
    O(n log n). Same idea as Meeting Rooms II.
    """
    order = sorted(range(len(tasks)), key=lambda i: (tasks[i][0], i))
    busy, free = [], []
    result = [0] * len(tasks)
    next_id = 0
    for i in order:
        start, duration = tasks[i]
        while busy and busy[0][0] <= start:
            heapq.heappush(free, heapq.heappop(busy)[1])
        if free:
            worker = heapq.heappop(free)
        else:
            worker = next_id
            next_id += 1
        result[i] = worker
        heapq.heappush(busy, (start + duration, worker))
    return result
