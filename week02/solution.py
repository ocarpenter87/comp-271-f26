"""
Solution for the Week 2 assignment: `Array271` -- a fixed-capacity array.

This file is a complete, standalone solution. It does not modify or
depend on `array_271.py` -- the assignment stub students work from -- so
that file stays untouched for students to complete themselves.

It re-implements the whole class (not just `resize`) so this file can be
read top to bottom on its own. The constructor and `add` are copied over
unchanged from the stub; only `resize` (and the small `ceiling` helper it
needs) are new.

The assignment requires "import nothing," so `resize` cannot reach for
`math.ceil`. The `ceiling` function below builds ceiling division from
first principles, using only the built-in `int()`.
"""


def ceiling(x):
    """Return the ceiling of x: the smallest integer that is >= x.

    We are not allowed to `import math` and use `math.ceil`, so we build
    ceiling from a more primitive tool: the built-in `int()`.

    Key fact this relies on: when `int()` converts a float to an int, it
    *truncates* -- it chops off everything after the decimal point,
    moving toward zero. For any x >= 0, moving toward zero is the same
    as rounding down, so `int(x)` gives us floor(x) for free.

    (This class only ever calls `ceiling()` with non-negative numbers --
    a capacity and a resize_factor are never negative -- so we don't
    need to worry about how truncation behaves for negative x, where it
    would round toward zero instead of down, and this simple formula
    would need adjusting.)

    Once we have floor(x) via `int(x)`, ceiling follows from a simple
    case split:

        - If x is already a whole number (x == int(x), e.g. x == 4.0),
          then x IS its own ceiling -- there's no fractional part to
          round up past.

        - Otherwise, x has a fractional part, so it sits strictly
          between int(x) and int(x) + 1 on the number line (e.g.
          x == 4.3 sits between 4 and 5). The smallest integer that is
          still >= x is therefore int(x) + 1.

    Examples:
        ceiling(0.5)  -> 1   (0.5 is between 0 and 1; round up to 1)
        ceiling(2.0)  -> 2   (already whole; stays 2)
        ceiling(1.25) -> 2   (between 1 and 2; round up to 2)
        ceiling(0.0)  -> 0   (already whole; stays 0)
    """
    truncated_toward_zero = int(x)  # == floor(x), since x >= 0 here

    if truncated_toward_zero != x:
        # x had a fractional part -- round up to the next whole number.
        truncated_toward_zero = truncated_toward_zero + 1

    return truncated_toward_zero


class Array271:
    """A fixed-capacity array of strings, backed by a Python list.

    See `array_271.py` for the full pedagogical writeup of what each
    field means and why this class exists. The short version:

        capacity (int): how many slots are currently reserved.
        occupancy (int): how many of those slots hold a real string.
        resize_factor (float): fraction of capacity to grow by when full.
        items (list): the underlying Python list used as raw storage.
    """

    def __init__(self, capacity: int = 2, resize_factor: float = 0.25):
        """Construct an empty Array271. Unchanged from the stub."""
        self.capacity: int = capacity
        self.resize_factor: float = resize_factor
        self.occupancy: int = 0
        self.items: list = [None] * capacity

    def add(self, value: str):
        """Add a string, growing the array first if it's full.

        Unchanged from the stub: check for room, resize if needed, place
        the value in the next free slot, and record that the slot is
        now taken.
        """
        if self.occupancy == self.capacity:
            self.resize()

        self.items[self.occupancy] = value
        self.occupancy += 1

    def resize(self):
        """Grow the array's capacity by (at least) `resize_factor`.

        Step 1: figure out how many *extra* slots to add.
        ---------------------------------------------------
        `resize_factor` is a fraction of the current capacity, e.g. 0.25
        means "grow by 25%." So the raw amount of growth is:

            growth = capacity * resize_factor

        This is a float, and it is very often NOT a whole number. With
        the class defaults (capacity=2, resize_factor=0.25):

            growth = 2 * 0.25 = 0.5

        You cannot allocate half a slot -- capacity has to be a whole
        number of slots -- so `growth` has to be rounded to an integer
        somehow. Rounding it *down* (0.5 -> 0) would mean "grow by zero
        slots," which defeats the entire purpose of resizing: the array
        would still be full immediately afterward, and the very next
        line in `add` (writing into `items[occupancy]`) would raise the
        same IndexError we were trying to fix.

        So we round UP instead, using the `ceiling` function above:

            additional_slots = ceiling(growth)   # ceiling(0.5) == 1

        Rounding up guarantees that as long as `growth` is greater than
        0, we add at least one real slot. As a final safety net -- in
        case someone constructs an Array271 with resize_factor=0, where
        growth is exactly 0.0 and ceiling(0.0) is legitimately 0 -- we
        clamp the result to a minimum of 1. `resize` is only ever called
        when the array is completely full, so it must always make room
        for at least one more item; otherwise `add` would break the
        moment resize_factor was 0.

        Step 2: allocate the new block and copy the old data over.
        ------------------------------------------------------------
        Just like a real fixed-capacity array, we cannot stretch the
        existing block in place -- the memory right after it might
        already belong to something else. So we allocate a brand-new
        list of the new, larger size (padded with None, same as
        `__init__` does), copy every currently-occupied string across
        one at a time, in order, and only then replace `self.items` and
        update `self.capacity`.

        We copy element-by-element -- rather than something like
        `new_items = self.items + [None] * additional_slots` -- because
        the whole point of this exercise is to make the copy step
        visible and explicit, the same way it would be if you were
        writing this in C: allocate new memory, copy old data into it,
        free/discard the old block.

        We also update `self.capacity` only at the very end, after the
        copy loop has finished. If we updated it first, the loop
        `range(self.occupancy)` wouldn't change (occupancy is untouched
        either way), but conceptually `self.capacity` would be lying
        about the size of `self.items` for the whole duration of the
        copy -- any code that ran in the middle (or a bug in the loop
        bounds) could read or write past the true end of the new list,
        or believe the resize had already succeeded when it hadn't.
        Finishing the copy first, then flipping both `self.items` and
        `self.capacity` together, keeps the object in a consistent
        state at every point an outside observer could see it.

        Note: `self.occupancy` is deliberately left untouched. Resizing
        changes how much ROOM there is, not how many strings are
        actually stored -- those are two different numbers, and this
        method only affects the first one.
        """
        # Step 1: how many extra slots do we need?
        growth = self.capacity * self.resize_factor
        additional_slots = ceiling(growth)
        if additional_slots < 1:
            additional_slots = 1  # always grow by at least one slot

        new_capacity = self.capacity + additional_slots

        # Step 2: allocate the new block, empty (None) in every slot.
        new_items = [None] * new_capacity

        # Step 3: copy every occupied string across, in order.
        for i in range(self.occupancy):
            new_items[i] = self.items[i]

        # Step 4: swap in the new block and record the new capacity.
        # (occupancy is intentionally untouched -- see docstring above.)
        self.items = new_items
        self.capacity = new_capacity


if __name__ == "__main__":
    # A tiny self-check, independent of test_array_271.py, that walks
    # through exactly the scenario the assignment README describes:
    # capacity=2, resize_factor=0.25, and a third `add` that forces a
    # resize.
    arr = Array271()  # capacity=2, resize_factor=0.25

    arr.add("this")
    arr.add("is")
    arr.add("full")  # occupancy (2) == capacity (2) -> triggers resize()

    assert arr.capacity == 3, f"expected capacity 3, got {arr.capacity}"
    assert arr.occupancy == 3
    assert arr.items == ["this", "is", "full"]

    print(f"capacity grew from 2 to {arr.capacity} after the third add")
    print("items:", arr.items)
    print("All checks in solution.py passed.")
