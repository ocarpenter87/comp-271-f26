"""
TwoDimensional: a data structure that stores strings in a grid of rows
and columns, spreadsheet style, and honors the OurContract interface.

Rows are labeled with numbers starting at 1. Columns are labeled with
letters starting at 'A', skipping I, O, and Z (they look too much like
1, 0, and 2/7). That leaves 23 letters:

    A B C D E F G H J K L M N P Q R S T U V W X Y

When there are more than 23 columns, labels continue with double
letters: AA, AB, ..., AY, BA, BB, ..., YY -- the same 23 letters, first
letter changing slowest. That makes 23 + 23 * 23 = 552 columns the most
this class supports.

Strings are added row-major: the first string goes to row 1, column A;
the second to row 1, column B; and so on across the row, then on to
row 2, column A.

The number of columns is fixed when the object is created. The number of
rows starts at 2 and grows, one row at a time, when the grid is full and
another string arrives.

Positions are reported as (row, column_label) pairs, e.g. (1, 'B').

Your job: replace every "TODO" below. Do not change the signatures.
Follow the course rules: one return statement per method, no break, no
imports beyond abc, typing, __future__, and OurContract, no magic numbers (use the constants).
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
        """
        # TODO
        pass

    def __position(self, p: int) -> tuple:
        """Return the (row, column_label) pair for flat index p, e.g. with
        4 columns, p = 5 is row 2, column 'B', so (2, 'B')."""
        # TODO
        pass

    def __grow(self) -> None:
        """Add one more row: allocate a bigger list, copy the old items,
        swap it in, and update the row count."""
        # TODO
        pass

    def add(self, value: str) -> None:
        # TODO: grow first if the grid is full, then store value in the
        # next free cell (row-major) and update occupancy.
        pass

    def contains(self, value: str) -> bool:
        # TODO: delegate to index_of, as we did in class.
        pass

    def index_of(self, value: str) -> tuple:
        # TODO: return the (row, column_label) pair of the FIRST cell
        # holding value, e.g. (1, 'B'), or an empty tuple () if value is
        # not present. Search only occupied cells.
        pass

    def indices(self, value: str) -> tuple:
        # TODO: return a tuple of the (row, column_label) pair of EVERY
        # cell holding value, in row-major order, e.g. ((1, 'B'), (3, 'A')),
        # or an empty tuple () if value is not present.
        pass

    def count(self, value: str) -> int:
        # TODO: how many occupied cells hold value.
        pass
