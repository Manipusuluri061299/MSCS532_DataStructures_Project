
import heapq
import itertools


class ReviewPriorityQueue:
    """Min-heap for scheduling policy reviews."""

    def __init__(self):
        self._heap = []
        self._sequence = itertools.count()

    def add_review(self, policy_id, priority):
        if not isinstance(priority, int) or isinstance(priority, bool):
            raise TypeError("Priority must be an integer")

        if priority < 1:
            raise ValueError("Priority must be at least 1")

        heapq.heappush(
            self._heap,
            (priority, next(self._sequence), policy_id),
        )

    def pop_next(self):
        if not self._heap:
            return None

        priority, _, policy_id = heapq.heappop(self._heap)
        return policy_id, priority

    def __len__(self):
        return len(self._heap)
