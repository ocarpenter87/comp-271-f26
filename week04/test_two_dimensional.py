"""
Plain-Python tests for TwoDimensional (two_dimensional.py).

No testing framework yet -- each test is a function that uses `assert`.
If an assert fails, Python raises AssertionError and tells you which
line failed.

How to run this file (from the folder holding two_dimensional.py and
OurContract.py):
    python3 test_two_dimensional.py

Until you implement the methods, most of these fail -- that's expected.
Work through them roughly top to bottom.
"""

from OurContract import OurContract
from two_dimensional import TwoDimensional


def position(result):
    """Normalize an index_of result so a tuple or a list both count."""
    return tuple(result)


def pairs(result):
    """Normalize an indices result: a tuple OR a list of (row, label) pairs."""
    assert isinstance(result, (tuple, list)), \
        "indices must return a tuple or a list"
    return tuple(tuple(pair) for pair in result)


def fill(td, n):
    """Add the strings "s0", "s1", ..., "s<n-1>" in that order."""
    for k in range(n):
        td.add("s" + str(k))


def test_implements_contract():
    assert issubclass(TwoDimensional, OurContract), \
        "TwoDimensional should inherit from OurContract"
    TwoDimensional()  # raises TypeError if a contract method is missing


def test_default_construction():
    td = TwoDimensional()
    assert td.get_columns() == 4, "default should be 4 columns"
    assert td.get_rows() == 2, "should start with 2 rows"
    assert td.get_occupancy() == 0, "should start empty"


def test_custom_columns():
    assert TwoDimensional(7).get_columns() == 7


def test_bad_columns_fall_back_to_default():
    assert TwoDimensional(0).get_columns() == 4, "0 columns is invalid"
    assert TwoDimensional(-3).get_columns() == 4, "negative is invalid"
    assert TwoDimensional(553).get_columns() == 4, "553 is over the limit"
    assert TwoDimensional(552).get_columns() == 552, "552 is allowed"


def test_add_is_row_major():
    td = TwoDimensional()
    for s in ["a", "b", "c", "d", "e"]:
        td.add(s)
    assert position(td.index_of("a")) == (1, "A"), "first string: row 1, column A"
    assert position(td.index_of("b")) == (1, "B"), "second string: row 1, column B"
    assert position(td.index_of("d")) == (1, "D"), "fourth string ends row 1"
    assert position(td.index_of("e")) == (2, "A"), "fifth string starts row 2"
    assert td.get_occupancy() == 5


def test_rows_grow_on_demand():
    td = TwoDimensional()
    fill(td, 8)
    assert td.get_rows() == 2, "8 strings still fit in 2 rows of 4"
    td.add("ninth")
    assert td.get_rows() == 3, "the ninth string needs a third row"
    assert position(td.index_of("ninth")) == (3, "A")
    assert position(td.index_of("s0")) == (1, "A"), "growing must keep old strings"
    assert position(td.index_of("s7")) == (2, "D"), "growing must keep old strings"
    assert td.get_columns() == 4, "columns never change"


def test_many_rows_grow():
    td = TwoDimensional(3)
    fill(td, 30)
    assert td.get_rows() == 10
    assert position(td.index_of("s29")) == (10, "C")


def test_labels_skip_i_o_and_z():
    td = TwoDimensional(23)
    fill(td, 23)
    assert position(td.index_of("s7")) == (1, "H")
    assert position(td.index_of("s8")) == (1, "J"), "no I"
    assert position(td.index_of("s12")) == (1, "N")
    assert position(td.index_of("s13")) == (1, "P"), "no O"
    assert position(td.index_of("s22")) == (1, "Y"), "23rd column is Y; no Z"


def test_double_letter_labels():
    td = TwoDimensional(30)
    fill(td, 30)
    assert position(td.index_of("s22")) == (1, "Y")
    assert position(td.index_of("s23")) == (1, "AA"), "24th column is AA"
    assert position(td.index_of("s24")) == (1, "AB")
    assert position(td.index_of("s29")) == (1, "AG")


def test_last_possible_column():
    td = TwoDimensional(552)
    fill(td, 553)
    assert position(td.index_of("s22")) == (1, "Y")
    assert position(td.index_of("s45")) == (1, "AY"), "AA..AY is 23 labels"
    assert position(td.index_of("s46")) == (1, "BA"), "then BA"
    assert position(td.index_of("s551")) == (1, "YY"), "552nd column is YY"
    assert position(td.index_of("s552")) == (2, "A")


def test_index_of_not_found():
    td = TwoDimensional()
    assert position(td.index_of("x")) == (), "empty grid: not found is ()"
    fill(td, 5)
    assert position(td.index_of("x")) == (), "absent value: not found is ()"


def test_index_of_returns_first_match():
    td = TwoDimensional()
    for s in ["p", "q", "x", "r", "x"]:
        td.add(s)
    assert position(td.index_of("x")) == (1, "C")


def test_index_of_ignores_empty_cells():
    td = TwoDimensional()
    td.add("a")
    assert position(td.index_of(None)) == (), "unused cells are not stored strings"


def test_contains():
    td = TwoDimensional()
    assert td.contains("a") is False, "empty grid contains nothing"
    td.add("a")
    td.add("b")
    assert td.contains("a") is True
    assert td.contains("b") is True
    assert td.contains("c") is False


def test_indices():
    td = TwoDimensional()
    for s in ["x", "y", "x", "z", "w", "x", "y"]:
        td.add(s)
    assert pairs(td.indices("x")) == ((1, "A"), (1, "C"), (2, "B")), \
        "every position, in row-major order"
    assert pairs(td.indices("y")) == ((1, "B"), (2, "C"))
    assert pairs(td.indices("w")) == ((2, "A"),), \
        "one match: a one-element tuple or list of one pair"
    assert pairs(td.indices("q")) == (), "no match: empty tuple or list"


def test_count():
    td = TwoDimensional()
    assert td.count("x") == 0
    for s in ["x", "y", "x", "z", "w", "x", "y"]:
        td.add(s)
    assert td.count("x") == 3
    assert td.count("y") == 2
    assert td.count("q") == 0


TESTS = [
    test_implements_contract,
    test_default_construction,
    test_custom_columns,
    test_bad_columns_fall_back_to_default,
    test_add_is_row_major,
    test_rows_grow_on_demand,
    test_many_rows_grow,
    test_labels_skip_i_o_and_z,
    test_double_letter_labels,
    test_last_possible_column,
    test_index_of_not_found,
    test_index_of_returns_first_match,
    test_index_of_ignores_empty_cells,
    test_contains,
    test_indices,
    test_count,
]

if __name__ == "__main__":
    failures = 0
    for test in TESTS:
        try:
            test()
            print("ok   ", test.__name__)
        except Exception as problem:
            failures += 1
            print("FAIL ", test.__name__, "-", repr(problem))
    print("All tests passed." if failures == 0
          else str(failures) + " test(s) failed.")
