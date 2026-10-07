"""
Solution for the Week 4 assignment: `TwoDimensional`, a grid of strings
that honors the `OurContract` interface.

This file is a complete, standalone solution. It does not modify or
depend on `two_dimensional.py` -- the assignment stub students work from
-- so that file stays untouched for students to complete themselves.

The class header, constants, constructor, and the three getters are
copied over unchanged from the stub. What's new here is everything that
was a `TODO`: `__column_label`, `__position`, `__grow`, `add`,
`contains`, `index_of`, `indices`, and `count`.

The design idea worth noticing: the whole grid lives in ONE flat list,
row-major, so "the next free cell" is always just index `occupancy`, and
a (row, column) pair is only ever computed on the way OUT of the class,
by `__position`. Nothing inside the class stores a row or a column for
any individual string.

Course rules followed throughout: one `return` per method (a result
variable set along the way), no `break`, no imports beyond `typing` and
`OurContract`, and no magic numbers -- the size of the alphabet comes
from `len(COLUMN_LETTERS)`, never a typed-in 23.

To check it, copy this file next to `OurContract.py` and
`test_two_dimensional.py`, rename it `two_dimensional.py`, and run
`python3 test_two_dimensional.py` -- all 16 tests should pass.
"""

from typing import Any

from OurContract import OurContract


class TwoDimensional(OurContract):

    COLUMN_LETTERS = "ABCDEFGHJKLMNPQRSTUVWXY"
    DEFAULT_COLUMNS = 4
    INITIAL_ROWS = 2
    MAX_COLUMNS = 552

    def __init__(self, columns: int = DEFAULT_COLUMNS):
        # If columns is out of range (fewer than 1 or more than
        # MAX_COLUMNS), quietly use DEFAULT_COLUMNS instead of crashing.
        valid = 1 <= columns <= TwoDimensional.MAX_COLUMNS
        self.__columns = columns if valid else TwoDimensional.DEFAULT_COLUMNS
        self.__rows = TwoDimensional.INITIAL_ROWS
        self.__occupancy = 0
        # One flat list holds the whole grid in row-major order, so the
        # cell at row r (0-based), column c (0-based) lives at
        # index r * columns + c.
        self.__items = [None] * (self.__rows * self.__columns)

    def get_columns(self) -> int:
        return self.__columns

    def get_rows(self) -> int:
        return self.__rows

    def get_occupancy(self) -> int:
        return self.__occupancy

    def __column_label(self, c: int) -> str:
        """Return the label for the 0-based column number c.

        0 -> 'A', 1 -> 'B', ..., 8 -> 'J' (no 'I'), ..., 22 -> 'Y',
        23 -> 'AA', 24 -> 'AB', ..., 551 -> 'YY'.

        The first len(COLUMN_LETTERS) columns get one letter. Past that,
        set those columns aside and read what's left as a two-digit
        number whose "digits" are the letters: the "tens" digit
        (// base) is the first letter, which changes slowest, and the
        "ones" digit (% base) is the second, which changes fastest.
        """
        letters = TwoDimensional.COLUMN_LETTERS
        base = len(letters)
        if c < base:
            label = letters[c]
        else:
            offset = c - base
            label = letters[offset // base] + letters[offset % base]
        return label

    def __position(self, p: int) -> tuple:
        """Return the (row, column_label) pair for flat index p, e.g. with
        4 columns, p = 5 is row 2, column 'B', so (2, 'B')."""
        # // counts the whole rows before p; rows are labeled from 1.
        row = p // self.__columns + 1
        # % is what's left over in that row: the 0-based column number.
        label = self.__column_label(p % self.__columns)
        return (row, label)

    def __grow(self) -> None:
        """Add one more row: allocate a bigger list, copy the old items,
        swap it in, and update the row count."""
        bigger = [None] * ((self.__rows + 1) * self.__columns)
        for p in range(self.__occupancy):
            bigger[p] = self.__items[p]
        self.__items = bigger
        self.__rows += 1

    def add(self, value: str) -> None:
        # Full means every cell is used: occupancy has reached the
        # length of the flat list.
        if self.__occupancy == len(self.__items):
            self.__grow()
        # The next free cell in row-major order is exactly index
        # `occupancy`.
        self.__items[self.__occupancy] = value
        self.__occupancy += 1

    def contains(self, value: str) -> bool:
        # An empty tuple means "not found"; anything else is a position.
        return self.index_of(value) != ()

    def index_of(self, value: str) -> tuple:
        # Only cells 0 .. occupancy - 1 hold strings; the rest are None
        # padding, so a search for None must not "find" them.
        result = ()
        p = 0
        # No `break`: the loop condition itself stops the search as soon
        # as result stops being the empty tuple.
        while p < self.__occupancy and result == ():
            if self.__items[p] == value:
                result = self.__position(p)
            p += 1
        return result

    def indices(self, value: str) -> tuple:
        result = ()
        for p in range(self.__occupancy):
            if self.__items[p] == value:
                # (pair,) -- the trailing comma makes a one-element
                # tuple to concatenate, so `result` stays a tuple of
                # pairs rather than a flat run of rows and labels.
                result = result + (self.__position(p),)
        return result

    def count(self, value: str) -> int:
        total = 0
        for p in range(self.__occupancy):
            if self.__items[p] == value:
                total += 1
        return total
