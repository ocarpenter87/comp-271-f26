"""
Plain-Python tests for TrainLine271 (train_line_271.py).

No testing framework yet -- each test is a function that uses `assert`.
If an assert fails, Python raises AssertionError and tells you which
line failed.

How to run this file (from the folder holding train_line_271.py,
Station.py, and OurContract.py):
    python3 test_train_line_271.py

Until you implement the methods, most of these fail -- that's expected.
Work through them roughly top to bottom.
"""

import time

from OurContract import OurContract
from train_line_271 import TrainLine271

RED_LINE_SOUTH = ["Howard", "Jarvis", "Morse", "Loyola", "Granville"]


def build(names):
    """Return a line holding the given station names, in order."""
    line = TrainLine271("test line")
    for name in names:
        line.add(name)
    return line


def as_list(result):
    """index_of and indices must return a list (contract update, 9/23)."""
    assert isinstance(result, list), \
        "index_of/indices should return a list, got " + type(result).__name__
    return result


def test_implements_contract():
    assert issubclass(TrainLine271, OurContract), \
        "TrainLine271 should inherit from OurContract"
    TrainLine271("Red")  # raises TypeError if a contract method is missing


def test_name_and_str():
    line = TrainLine271("Red Line southbound")
    assert line.get_name() == "Red Line southbound"
    assert "Red Line southbound" in str(line)


def test_empty_line():
    line = TrainLine271("empty")
    assert line.contains("Howard") is False, "an empty line contains nothing"
    assert as_list(line.index_of("Howard")) == [], \
        "not found should be an empty list"
    assert as_list(line.indices("Howard")) == []
    assert line.count("Howard") == 0


def test_first_station():
    line = build(["Howard"])
    assert line.contains("Howard") is True
    assert as_list(line.index_of("Howard")) == [0], \
        "the head is at position 0"


def test_add_keeps_order():
    line = build(RED_LINE_SOUTH)
    for position, name in enumerate(RED_LINE_SOUTH):
        assert as_list(line.index_of(name)) == [position], \
            name + " should be at position " + str(position)


def test_contains():
    line = build(RED_LINE_SOUTH)
    assert line.contains("Loyola") is True
    assert line.contains("Granville") is True, "last station counts too"
    assert line.contains("Union Station") is False
    assert line.contains("loyola") is False, "names are case-sensitive"


def test_index_of_missing():
    line = build(RED_LINE_SOUTH)
    assert as_list(line.index_of("Union Station")) == []


def test_index_of_returns_first_match():
    line = build(["Clark/Lake", "State/Lake", "Clark/Lake"])
    assert as_list(line.index_of("Clark/Lake")) == [0], \
        "index_of stops at the first match"


def test_indices():
    line = build(["b", "a", "n", "a", "n", "a"])
    assert as_list(line.indices("a")) == [1, 3, 5]
    assert as_list(line.indices("n")) == [2, 4]
    assert as_list(line.indices("b")) == [0], \
        "a single match is still a one-element list"
    assert as_list(line.indices("z")) == []


def test_count():
    line = build(["b", "a", "n", "a", "n", "a"])
    assert line.count("a") == 3
    assert line.count("b") == 1
    assert line.count("z") == 0


def test_searches_do_not_change_the_line():
    line = build(RED_LINE_SOUTH)
    line.index_of("Morse")
    line.indices("Morse")
    line.count("Morse")
    line.contains("Morse")
    assert as_list(line.indices("Howard")) == [0]
    assert as_list(line.index_of("Granville")) == [4]


def test_add_after_search():
    line = build(RED_LINE_SOUTH)
    line.contains("Morse")
    line.add("Thorndale")
    assert as_list(line.index_of("Thorndale")) == [5], \
        "a new station goes after the old last station"
    assert as_list(line.index_of("Howard")) == [0], \
        "the head does not move"


def test_add_takes_constant_time():
    """Adding to a long line should cost about the same as adding to a
    short one. If add walks from the head every time (the old TrainLine),
    building the long line takes far longer than ten times the short one."""
    short, long = 2_000, 20_000

    start = time.perf_counter()
    build(["s" + str(k) for k in range(short)])
    short_time = time.perf_counter() - start

    start = time.perf_counter()
    long_line = build(["s" + str(k) for k in range(long)])
    long_time = time.perf_counter() - start

    assert long_time < 30 * short_time + 0.05, \
        "add seems to walk the whole line -- use the last pointer"
    assert as_list(long_line.index_of("s" + str(long - 1))) == [long - 1]


TESTS = [
    test_implements_contract,
    test_name_and_str,
    test_empty_line,
    test_first_station,
    test_add_keeps_order,
    test_contains,
    test_index_of_missing,
    test_index_of_returns_first_match,
    test_indices,
    test_count,
    test_searches_do_not_change_the_line,
    test_add_after_search,
    test_add_takes_constant_time,
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
