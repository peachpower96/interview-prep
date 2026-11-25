"""Leaderboard (LeetCode 1244).

add_score and reset are O(1). top(k) is O(n log k) with heapq.nlargest,
instead of O(n log n) for sorting every total.
Assumption to say out loud: scores are positive, so removing a player and
zeroing a player give the same top(k).
"""
import heapq


class Leaderboard:
    def __init__(self):
        self.scores = {}  # player -> running total

    def add_score(self, player_id, score):
        self.scores[player_id] = self.scores.get(player_id, 0) + score

    def top(self, k):
        """Sum of the k highest totals (fewer players: sum them all)."""
        return sum(heapq.nlargest(k, self.scores.values()))

    def reset(self, player_id):
        self.scores.pop(player_id, None)
