"""
Week 8 scaffold.

Part 1: merge_sort_iterative -- convert the recursive merge_sort into a
bottom-up version with no recursion.
Part 2: ArrayQueue271 (circular) and ArrayStack271, both built on a plain
fixed-capacity array (a Python list that never changes size).

Same convention as every assignment this term: each function/method has
exactly ONE return statement. Set a result variable to its "failed" /
fallback value first, and only overwrite it once the guard condition passes.
"""

from __future__ import annotations


# ---------------------------------------------------------------- Part 1

def merge(a: list[int], b: list[int]) -> list[int]:
    """Merge two already-sorted lists into one new sorted list.

    Given -- the same merge from class, with the print statements removed.
    """
    c: list[int] = []
    i = j = 0
    while i < len(a) and j < len(b):
        if a[i] < b[j]:
            c.append(a[i])
            i += 1
        else:
            c.append(b[j])
            j += 1
    while i < len(a):
        c.append(a[i])
        i += 1
    while j < len(b):
        c.append(b[j])
        j += 1
    return c


def merge_sort(arr: list[int]) -> list[int]:
    """Recursive merge sort, as written in class. Returns a new list.

    Given -- read it closely; your job is to produce the same result
    without any function calling itself.
    """
    result = arr
    if len(arr) > 1:
        mid = len(arr) // 2
        sorted_left = merge_sort(arr[:mid])
        sorted_right = merge_sort(arr[mid:])
        result = merge(sorted_left, sorted_right)
    return result


def merge_sort_iterative(arr: list[int]) -> list[int]:
    """Bottom-up merge sort: no recursion. Returns a NEW sorted list and
    leaves arr unchanged.

    Use the given merge() for the merging itself. Do not call merge_sort
    (or this function) from in here, and do not use sorted() or .sort().
    """
    result = list(arr)
    # TODO: repeatedly merge neighboring runs, doubling the run width each pass
    return result


# ---------------------------------------------------------------- Part 2

class ArrayQueue271:
    """FIFO queue on a fixed-capacity array that wraps around.

    front -- index of the next item to remove
    back  -- index where the next item will be written
    used  -- how many items are currently stored
    """

    def __init__(self, capacity: int = 4):
        self.capacity: int = capacity
        self.storage: list = [None] * capacity
        self.front: int = 0
        self.back: int = 0
        self.used: int = 0

    def __len__(self) -> int:
        return self.used

    def is_empty(self) -> bool:
        return self.used == 0

    def is_full(self) -> bool:
        return self.used == self.capacity

    def add(self, item) -> bool:
        """Add item at the back. Return True if added; if the queue is
        full, change nothing and return False."""
        added = False
        # TODO
        return added

    def remove(self):
        """Remove and return the front item. If the queue is empty,
        change nothing and return None."""
        item = None
        # TODO
        return item

    def __str__(self) -> str:
        return f"{self.storage} front={self.front} back={self.back} used={self.used}"


class ArrayStack271:
    """LIFO stack on a fixed-capacity array, filled from the back
    (index capacity - 1) toward index 0.

    top  -- index where the next item will be written
    used -- how many items are currently stored
    """

    def __init__(self, capacity: int = 4):
        self.capacity: int = capacity
        self.storage: list = [None] * capacity
        self.top: int = capacity - 1
        self.used: int = 0

    def __len__(self) -> int:
        return self.used

    def is_empty(self) -> bool:
        return self.used == 0

    def is_full(self) -> bool:
        return self.used == self.capacity

    def add(self, item) -> bool:
        """Push item. Return True if added; if the stack is full, change
        nothing and return False."""
        added = False
        # TODO
        return added

    def remove(self):
        """Pop and return the most recently added item. If the stack is
        empty, change nothing and return None."""
        item = None
        # TODO
        return item

    def __str__(self) -> str:
        return f"{self.storage} top={self.top} used={self.used}"
