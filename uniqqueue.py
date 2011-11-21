"""
A simple unique queue.
No item is ever inserted more than once.
"""

from collections import deque

class UniqQueue:
    def __init__(self, initial_elements=[]):
        assert isinstance(initial_elements, list)
        self.q = deque()
        self.seen = {}
        self.extend(initial_elements)

    def append(self, i):
        if i not in self.seen:
            self.q.append(i)
            self.seen[i] = True
        assert i in self.seen

    def extend(self, lst):
        for i in lst: self.append(i)

    def pop(self):
        return self.q.popleft()

    def empty(self):
        return len(self.q) == 0
