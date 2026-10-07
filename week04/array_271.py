# ============================================================================
# NOTE ON TYPE HINTS
# ----------------------------------------------------------------------------
# The type hints in this file (e.g. "i: int", "-> bool") are for
# DEMONSTRATION / ILLUSTRATIVE purposes only. Python does not enforce them
# at runtime -- they are documentation for readers and tools like mypy, not
# a guarantee. Passing an argument of the "wrong" type will not raise an
# error on its own.
# ============================================================================

# Week 04 version
# Array-backed implementation of the OurContract interface. Storage grows
# automatically as items are added; it never shrinks back down.
from abc import abstractmethod
from math import ceil
from OurContract import OurContract

class Array271(OurContract):

    def __init__(self, capacity: int = 2, resize_factor: float = 0.25):
        # capacity: how many slots __items currently has (used + free)
        # resize_factor: fraction to grow by when add() runs out of room
        # occupancy: how many slots are actually holding a value
        self._capacity: int = capacity
        self._resize_factor: float = resize_factor
        self._occupancy: int = 0
        self._items: list = [None] * capacity

    def __str__(self) -> str:
        """Return a human-readable summary: capacity, occupancy, and the
        occupied slots only (not the trailing Nones)."""
        occupied = self._items[: self._occupancy]
        return (
            f"Array271(capacity={self._capacity}, "
            f"occupancy={self._occupancy}, items={occupied})"
        )

    # ------------------------------------------------------------------
    # Accessors -- the only sanctioned way to read a private attribute
    # from outside the class.
    # ------------------------------------------------------------------

    def get_capacity(self) -> int:
        return self._capacity

    def get_resize_factor(self) -> float:
        return self._resize_factor

    def get_occupancy(self) -> int:
        return self._occupancy

    def get_items(self) -> list:
        return self._items

    def get_item(self, i: int):
        # Bounds-checked read: out-of-range indices return None instead
        # of raising, so callers don't have to guard every access.
        item = None
        if 0 <= i < self._occupancy:
            item = self._items[i]
        return item



    # ------------------------------------------------------------------
    # Mutators
    # ------------------------------------------------------------------


    def add(self, value: str):
        # Grow first if the array is full, then append at the next free
        # slot (index == current occupancy) and bump occupancy by one.
        if self._occupancy == self._capacity:
            self.__resize()
        self._items[self._occupancy] = value
        self._occupancy += 1

    def __resize(self) -> None:
        # Grow capacity by resize_factor (e.g. 0.25 == 25% bigger),
        # rounding up so capacity always increases by at least one slot.
        # Copies existing items into a fresh, larger list.
        growth = ceil(self._capacity*(1+self._resize_factor))
        temp = [None] * growth
        for i in range(self._capacity):
            temp[i] = self._items[i]
        self._items = temp
        self._capacity = growth


    def remove(self, i: int) -> bool:
        # Clears the slot at index i (sets it to None) but does not
        # shift later items down or decrement occupancy.
        success = i >= 0 and i < self._occupancy
        if success:
            self._items[i] = None
        return success

    def contains(self,value: str) -> bool:
        # Stub: always reports True, and is still missing the value
        # parameter required by the contract. Needs to actually search
        # _items for value and return whether it was found.
        """
        found = False
        i = 0
        while i < self._occupancy and not found:
            found = self._items[i] == value
            i += 1
        return found
        """
        return len(self.index_of(value)) > 0

    
    def index_of(self, value: str) -> tuple:
        # Linear search from the front; returns the first matching
        # index as a one-element tuple, e.g. (2,), or an empty tuple ()
        # if value is never found among occupied slots.
        result = ()
        i = 0
        while i < self._occupancy and len(result) == 0:
            if self._items[i] == value:
                # The trailing comma is what makes this a tuple. Parentheses
                # alone do nothing: (i) is just the integer i, the same way
                # (2 + 3) is just 5. A one-element tuple needs the comma,
                # (i,), so the caller always gets a tuple back, never an int.
                result = (i,)
            i = i + 1
        return result


    def indices(self, value: str) -> tuple:
        # Linear search over the occupied slots only; collects every
        # matching index, front to back, into an immutable tuple.
        result = ()
        for i in range(self._occupancy):
            if self._items[i] == value:
                # (i,) is a one-element tuple; the comma is required (plain
                # (i) is just the integer i). Tuples are immutable, so "+"
                # builds a new, longer tuple rather than changing the old one.
                result = result + (i,)
        return result


    def count(self, value: str) -> int:
        # Stub: should count how many occupied slots equal value
        # (like list.count), not return a hardcoded placeholder number.
        count = 0
        for i in range(self._occupancy):
            #if self._items[i] == value:
            #    count +=1
            count = count+1 if self._items[i] == value else count
        return count

# Quick manual smoke test when this file is run directly.
if __name__ == "__main__":
    print("Quick manual smoke test of Array271 class...")
    test = Array271()
    print(test)
    test.add("a")
    test.add("b")
    test.add("c")
    print(test)
    print(f"index_of('b') = {test.index_of('b')}")
    print(f"index_of('z') = {test.index_of('z')}")
    print(f"count() = {test.count('a')}") 