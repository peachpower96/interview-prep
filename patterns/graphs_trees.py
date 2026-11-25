"""Grid BFS/DFS and an iterative tree check. Multi-source grid BFS lives in
coding/grid_bfs_rotting_oranges."""
from collections import deque


def shortest_route(grid, start, goal):
    """Fewest up/down/left/right moves on a grid of '.' (open) and '#' (blocked); -1 if none.

    BFS with a deque of (row, col, dist) and a seen set; mark seen when ADDING to the queue.
    BFS gives shortest paths only when every move costs the same; for weighted moves use
    Dijkstra (heapq of (cost, row, col)). O(rows * cols).
    """
    rows, cols = len(grid), len(grid[0])
    queue = deque([(start[0], start[1], 0)])
    seen = {start}
    while queue:
        r, c, dist = queue.popleft()
        if (r, c) == goal:
            return dist
        for dr, dc in ((1, 0), (-1, 0), (0, 1), (0, -1)):
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr][nc] == "." and (nr, nc) not in seen:
                seen.add((nr, nc))
                queue.append((nr, nc, dist + 1))
    return -1


def count_regions(grid):
    """Number of 4-connected regions of '.' cells (diagonals do not connect).

    Scan every cell; on an unseen '.', count one and flood-fill its region. This recursive
    flood fill can hit Python's recursion limit (~1000) on long winding regions; for real
    inputs use an explicit stack. O(rows * cols).
    """
    if not grid:
        return 0
    rows, cols = len(grid), len(grid[0])
    seen = set()

    def flood(r, c):
        if r < 0 or r >= rows or c < 0 or c >= cols:
            return
        if grid[r][c] != "." or (r, c) in seen:
            return
        seen.add((r, c))
        flood(r + 1, c)
        flood(r - 1, c)
        flood(r, c + 1)
        flood(r, c - 1)

    regions = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == "." and (r, c) not in seen:
                regions += 1
                flood(r, c)
    return regions


def is_valid_bst(root):
    """root is (value, left, right) or None. Strictly increasing in-order => valid BST.

    Iterative in-order with an explicit stack (no recursion limit). Use `prev is not None`,
    not truthiness, so a value of 0 still counts. Checking only each node against its direct
    children misses deep violations. O(n) time, O(height) space.
    """
    stack = []
    node = root
    prev = None
    while stack or node is not None:
        while node is not None:
            stack.append(node)
            node = node[1]
        node = stack.pop()
        if prev is not None and node[0] <= prev:
            return False
        prev = node[0]
        node = node[2]
    return True
