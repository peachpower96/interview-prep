"""Rotting oranges (LeetCode 994): multi-source BFS, one level per minute.

0 = empty, 1 = fresh, 2 = rotten. Each minute, fresh cells next to a rotten
cell (up/down/left/right) rot. Return minutes until none are fresh, or -1.

Pattern: start the BFS from ALL rotten cells at once; count fresh cells up
front so -1 is detected without a second scan. O(rows * cols) time and space.
"""
from collections import deque


def minutes_to_rot(grid):
    grid = [row[:] for row in grid]   # work on a copy; do not mutate the caller's grid
    rows, cols = len(grid), len(grid[0])
    queue = deque()
    fresh = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 2:
                queue.append((r, c))
            elif grid[r][c] == 1:
                fresh += 1

    minutes = 0
    while queue and fresh > 0:
        for _ in range(len(queue)):   # everything rotten right now = one minute
            r, c = queue.popleft()
            for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == 1:
                    grid[nr][nc] = 2
                    fresh -= 1
                    queue.append((nr, nc))
        minutes += 1
    return minutes if fresh == 0 else -1
