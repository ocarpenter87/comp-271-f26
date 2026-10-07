"""
Solution for the Week 3 assignment: `Array271.remove`, plus splitting
`_resize` into `__upsize`/`__downsize`.

This file is a complete, standalone solution. It does not modify or
depend on `array_271.py` -- the assignment stub students work from -- so
that file stays untouched for students to complete themselves.

It re-implements the whole class (not just the three assigned changes)
so this file can be read top to bottom on its own. `__init__`, the
getters, and `add` are copied over unchanged from the stub. `__str__` is
ALSO left unchanged on purpose, even though it doesn't slice
`self.__items` down to `self.__occupancy` and so still prints trailing
`None` padding -- the assignment explicitly says not to touch `__str__`,
and this solution follows that instruction to the letter rather than
quietly fixing it. (That's also why `test_str_shows_occupied_items_only`
fails against this file, exactly as it does against the unmodified
starting file -- a known, pre-existing gap in this week's scaffold, not
something `remove`/`__upsize`/`__downsize` are supposed to paper over.)

What's actually new here: `remove` returns the removed item and closes
the gap by shifting, and `_resize` is retired in favor of two focused,
name-mangled methods, `__upsize` (same logic as `_resize`, new name) and
`__downsize` (new).
"""

from math import ceil

# How full the array must stay before `remove` bothers shrinking it.
# "Roughly below 50% usage," per the assignment -- pinned here as an
# actual number so `remove` has something concrete to compare against.
DOWNSIZE_THRESHOLD = 0.5

# `__downsize` never lets capacity drop below this, no matter how empty
# the array gets -- a capacity of 0 would make the next `add` immediately
# call `__upsize` again with nothing to grow from, and a capacity of 1
# still gives `add` exactly one free slot to write into before it has to
# grow. Keeping a capacity of 1 as the floor means "empty but ready,"
# never "no room to exist at all."
MIN_CAPACITY = 1


class Array271:
    """A fixed-capacity array of strings, backed by a Python list.

    See `array_271.py` for the full pedagogical writeup of what each
    private attribute means and why this class exists. The short
    version:

        __capacity (int): how many slots are currently reserved.
        __resize_factor (float): fraction of capacity to grow/shrink by.
        __occupancy (int): how many of those slots hold a real string.
        __items (list): the underlying Python list used as raw storage.

    Every attribute is name-mangled (double leading underscore) rather
    than just conventionally private (single underscore) -- the
    distinction this week's class discussion was about. `__upsize` and
    `__downsize` follow the same convention: they're implementation
    details `add` and `remove` lean on, not part of the public interface.
    """

    def __init__(self, capacity: int = 2, resize_factor: float = 0.25):
        """Create an empty array with the given starting capacity.

        Unchanged from the stub.
        """
        self.__capacity: int = capacity
        self.__resize_factor: float = resize_factor
        self.__occupancy: int = 0
        self.__items: list = [None] * capacity

    def __str__(self):
        """Return a human-readable summary of the array's internal state.

        Deliberately unchanged from the stub -- the assignment says not
        to touch `__str__`, so this still prints the full backing list,
        trailing `None` padding included. See the module docstring for
        why that's expected, not a bug in this solution.
        """
        return f"Array271(capacity={self.__capacity}, resize_factor={self.__resize_factor}, occupancy={self.__occupancy}, items={self.__items})"

    def get_capacity(self):
        """Return the total number of slots currently allocated."""
        return self.__capacity

    def get_resize_factor(self):
        """Return the fraction by which capacity grows/shrinks on resize."""
        return self.__resize_factor

    def get_occupancy(self):
        """Return the number of slots currently holding a value."""
        return self.__occupancy

    def get_items(self):
        """Return the underlying list, including any unused (None) slots."""
        return self.__items

    def get_item(self, i):
        """Return the value at index `i`, or None if `i` is out of bounds.

        Unchanged from the stub.
        """
        item = None
        if i >= 0 and i < self.__occupancy:
            item = self.__items[i]
        return item

    # ------------------------------------------------------------------
    # Mutators
    # ------------------------------------------------------------------

    def add(self, value: str):
        """Append `value` to the first free slot, growing first if full.

        Only change from the stub: calls `__upsize()` where the stub
        called `_resize()` -- same moment, same job, new name.
        """
        if self.__occupancy == self.__capacity:
            self.__upsize()
        self.__items[self.__occupancy] = value
        self.__occupancy += 1

    def __upsize(self):
        """Grow capacity by `resize_factor`, copying existing items over.

        This is `_resize` from the stub, renamed and otherwise untouched
        -- same formula, same copy loop, same "update capacity only after
        the copy finishes" ordering. See `remove`'s docstring below and
        `__downsize` for how this logic now has a mirror image.

        Capacity always grows by at least one slot: `ceil` guarantees
        that even a tiny resize_factor (or capacity of 1) still makes
        room for the pending `add` -- growth = capacity * resize_factor
        is very often a fraction (e.g. 2 * 0.25 = 0.5 slots), and
        rounding a fraction *down* to 0 extra slots would defeat the
        whole point of resizing.
        """
        growth = ceil(self.__capacity * (1 + self.__resize_factor))
        temp = [None] * growth
        for i in range(self.__capacity):
            temp[i] = self.__items[i]
        self.__items = temp
        self.__capacity = growth

    def __downsize(self):
        """Shrink capacity by `resize_factor`, copying occupied items over.

        The mirror image of `__upsize`: same shape (allocate a new list
        at the new size, copy the live data across, swap it in), just
        shrinking instead of growing. Two differences from `__upsize`,
        both there to keep the array from ever losing data or becoming
        unusable:

        1. We only copy `__occupancy` items, not `__capacity` -- there's
           no reason to copy the empty, already-None tail of the old
           list into the new one.
        2. The new capacity is clamped with `max(...)` so it can never
           drop below two things: `__occupancy` (we must never shrink
           past the number of items we're actually holding -- that would
           silently drop data) or `MIN_CAPACITY` (an array should always
           have at least one slot to grow from, never zero).

        `ceil` is used here for the same reason `__upsize` uses it: a
        fractional shrink amount should round toward *less* aggressive
        shrinking, not more, so a small `resize_factor` doesn't
        accidentally shrink the array further than intended.
        """
        shrunk = ceil(self.__capacity * (1 - self.__resize_factor))
        shrunk = max(shrunk, self.__occupancy, MIN_CAPACITY)

        temp = [None] * shrunk
        for i in range(self.__occupancy):
            temp[i] = self.__items[i]
        self.__items = temp
        self.__capacity = shrunk

    def remove(self, i):
        """Remove and return the value at index `i`, closing the gap.

        Three things changed from the stub's `remove`, all three parts
        of this week's assignment:

        1. Returns the removed string itself, not a True/False flag.
           `removed` starts as `None` and only gets overwritten if `i`
           is actually a valid, occupied index -- so `None` doubles as
           "nothing was removed," and a caller can tell that apart from
           an item that happened to be an empty string, since `None` is
           never itself a valid string.

        2. Shifts every item after `i` down by one slot, so occupied
           slots stay contiguous starting at index 0 -- the invariant
           `add` depends on, since `add` always writes to
           `items[occupancy]`. The shift loop runs from `i` up to (but
           not including) the *old* `occupancy - 1`, which is exactly
           why the shift happens BEFORE `occupancy` is decremented: the
           loop needs the old occupancy to know where the last occupied
           item currently is. Decrementing first would shrink the loop's
           range by one and leave the last real item un-shifted.

        3. Once occupancy drops below `DOWNSIZE_THRESHOLD` of capacity,
           shrinks the array via `__downsize()` -- the mirror of how
           `add` grows the array via `__upsize()`.
        """
        removed = None

        if i >= 0 and i < self.__occupancy:
            removed = self.__items[i]

            # Shift every item after i down by one, closing the hole.
            # Uses the OLD occupancy as the upper bound -- see point 2
            # above for why this has to happen before occupancy changes.
            for j in range(i, self.__occupancy - 1):
                self.__items[j] = self.__items[j + 1]

            # The old last occupied slot is now a duplicate; clear it.
            self.__items[self.__occupancy - 1] = None

            self.__occupancy -= 1

            if self.__occupancy < self.__capacity * DOWNSIZE_THRESHOLD:
                self.__downsize()

        return removed


if __name__ == "__main__":
    # A tiny self-check, independent of test_array_271.py, that exercises
    # all three assigned changes: remove returning the item, the shift
    # closing the gap, and a downsize actually triggering.
    arr = Array271(capacity=4, resize_factor=0.25)
    arr.add("kale")
    arr.add("turnip")
    arr.add("eggplant")

    removed = arr.remove(0)
    assert removed == "kale", f"expected 'kale', got {removed!r}"
    assert arr.get_occupancy() == 2, "occupancy should drop to 2"
    assert arr.get_item(0) == "turnip", "turnip should have shifted into slot 0"
    assert arr.get_item(1) == "eggplant", "eggplant should have shifted into slot 1"

    # occupancy (2) < capacity (4) * DOWNSIZE_THRESHOLD (0.5) -> 2 < 2 is
    # False, so no downsize yet after that first remove. One more should
    # push occupancy below the threshold and trigger a shrink.
    assert arr.get_capacity() == 4, "capacity should not have shrunk yet"

    arr.remove(0)  # occupancy now 1; 1 < 4 * 0.5 -> downsize should fire
    assert arr.get_capacity() < 4, "capacity should have shrunk"
    assert arr.get_occupancy() == 1
    assert arr.get_item(0) == "eggplant"

    # Removing an invalid index should fail gracefully, not crash.
    assert arr.remove(99) is None, "an out-of-range remove should return None"

    print(f"final capacity: {arr.get_capacity()}, occupancy: {arr.get_occupancy()}")
    print("items:", arr.get_items())
    print("All checks in solution.py passed.")
