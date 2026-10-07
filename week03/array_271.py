"""
Array271 -- a fixed-capacity string array, built on top of a Python list.

This is the Week 2 `Array271` (see `week02/array_271.py`) carried forward
and extended with what we covered in class this week: private attributes
with accessor ("getter") methods instead of reaching into the object
directly, a `__str__` so printing an object shows something useful, a
`resize` that actually works, and a first `remove`.

Encapsulation, in short: every attribute is named with a leading
underscore (`_capacity`, not `capacity`) as a signal of "please don't
reach in here directly" -- Python doesn't enforce this, unlike Java or
C++, so it's a convention we agree to respect, not a wall. Reading or
changing an attribute from outside the class should always go through a
method (a getter, or a method like `add` that changes state on your
behalf).

This file is intentionally incomplete in one place: `remove` works, but
only partially -- see its docstring, and this week's `README.md`, for the
two modifications that are your assignment.
"""

from math import ceil


class Array271:
    """A fixed-capacity array of strings, backed by a Python list.

    Private attributes (leading underscore -- see module docstring):

        _capacity (int):
            How many string slots this array currently has room for,
            whether they're all in use or not.

        _resize_factor (float):
            How aggressively the array grows when it runs out of room.
            Expressed as a fraction of the current capacity to add, e.g.
            0.25 means "grow capacity by 25% when you resize."

        _occupancy (int):
            How many slots are actually holding a string right now.
            Always satisfies 0 <= occupancy <= capacity.

        _items (list):
            The underlying Python list that actually stores the strings.
            Pre-sized to `_capacity` and padded with None past the last
            occupied slot -- treat index `_occupancy` and beyond as empty,
            even though Python itself doesn't enforce that for us.
    """

    def __init__(self, capacity: int = 2, resize_factor: float = 0.25):
        """Create an empty array with the given starting capacity.

        Args:
            capacity (int): Number of slots to allocate up front.
            resize_factor (float): Growth fraction used by `__resize`.
        """
        # total slots allocated
        self.__capacity: int = capacity
        # growth rate used by __resize
        self.__resize_factor: float = resize_factor
        # no items stored yet
        self.__occupancy: int = 0
        # pre-sized, None-padded past occupancy
        self.__items: list = [None] * capacity

    def __str__(self):
        """Return a human-readable summary of the array's internal state."""
        return f"Array271(capacity={self.__capacity}, resize_factor={self.__resize_factor}, occupancy={self.__occupancy}, items={self.__items})"

    def get_capacity(self):
        """Return the total number of slots currently allocated."""
        return self.__capacity
    def get_resize_factor(self):
        """Return the fraction by which capacity grows on resize."""
        return self.__resize_factor
    def get_occupancy(self):
        """Return the number of slots currently holding a value."""
        return self.__occupancy
    def get_items(self):
        """Return the underlying list, including any unused (None) slots."""
        return self.__items

    def get_item(self, i):
        """Return the value at index `i`, or None if `i` is out of bounds.

        Bounds are checked against occupancy, not capacity, so indices
        pointing at allocated-but-unused slots also return None.
        """
        # default result for an out-of-bounds index
        item = None
        # only occupied slots are valid
        if i >=0 and i < self.__occupancy:
            # fetch the value at that slot
            item = self.__items[i]
        return item


    # ------------------------------------------------------------------
    # Mutators
    # ------------------------------------------------------------------

    def add(self, value: str):
        """Append `value` to the first free slot, growing first if full."""
        # no free slots left
        if self.__occupancy == self.__capacity:
            # make room before writing
            self.__resize()
        # write into the next free slot
        self.__items[self.__occupancy] = value
        # one more slot is now in use
        self.__occupancy += 1

    def __resize(self):
        """Grow capacity by `resize_factor`, copying existing items over.

        Capacity always grows by at least one slot: `ceil` guarantees
        that even a tiny resize_factor (or capacity of 1) still makes
        room for the pending `add`.
        """
        # new, larger capacity
        growth = ceil(self.__capacity*(1+self.__resize_factor))
        # new backing list, bigger than the old one
        temp = [None] * growth
        # copy every existing item over
        for i in range(self.__capacity):
            temp[i] = self.__items[i]
        # swap in the bigger list
        self.__items = temp
        # record the new capacity
        self.__capacity = growth



    def remove(self, i):
        """Clear the value at index `i`, leaving a gap instead of shifting.

        Note: this only blanks the slot to None -- it does not shift
        later items left or decrement occupancy, so occupancy and the
        "no gaps before occupancy" invariant described in the class
        docstring can end up violated. See README.md for this week's
        assignment to fix that.
        """
        # only occupied slots can be removed
        success = i >= 0 and i < self.__occupancy
        if success:
            # blank the slot (leaves a gap -- see docstring)
            self.__items[i] = None
        return success
