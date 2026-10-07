"""
Plain-Python tests for BetterTrainLine (better_train_line_271.py).

No testing framework yet -- each test is a function that uses `assert`.
If an assert fails, Python raises AssertionError and tells you which
line failed.

How to run this file (from the folder holding better_train_line_271.py
and Station.py):
    python3 test_better_train_line_271.py

find_e_f_station is TODO -- its tests are expected to fail (or crash
with AttributeError, if you haven't added the method yet) until you
implement it. Everything else should already pass against the given
code.
"""

import ast
import inspect
import textwrap

from Station import Station
from better_train_line_271 import BetterTrainLine

RED_LINE_SOUTH = ["Howard", "Jarvis", "Morse", "Loyola", "Granville"]

# A 7-station line, picked so e/f positions land cleanly (no rounding
# ambiguity) for the (e, f) pairs this file checks.
SEVEN_STATIONS = ["A", "B", "C", "D", "E", "F", "G"]


def build(names):
    """Return a line holding one Station per name, added in order."""
    line = BetterTrainLine("test line")
    for name in names:
        line.add(Station(name))
    return line


def names_of(line):
    """get_names(), but fails loudly with a clear message if it's not
    returning a list yet."""
    result = line.get_names()
    assert isinstance(result, list), \
        "get_names should return a list, got " + type(result).__name__
    return result


def code_source_of(method):
    """Return method's source with its docstring stripped, so a check
    against the code itself isn't tripped up by the docstring merely
    talking about what the code shouldn't do."""
    source = textwrap.dedent(inspect.getsource(method))
    body = ast.parse(source).body[0].body
    has_docstring = (
        body
        and isinstance(body[0], ast.Expr)
        and isinstance(body[0].value, ast.Constant)
        and isinstance(body[0].value.value, str)
    )
    if has_docstring:
        body = body[1:]
    return "\n".join(ast.get_source_segment(source, node) for node in body)


def source_avoids(method, forbidden_substrings):
    """True if none of forbidden_substrings appear in method's code
    (docstring excluded)."""
    code = code_source_of(method)
    return all(text not in code for text in forbidden_substrings)


def test_add_single_station():
    line = build(["Howard"])
    assert line.find_middle_station().get_name() == "Howard", \
        "a one-station line's middle station is its only station"


def test_get_names_on_built_line():
    line = build(RED_LINE_SOUTH)
    assert names_of(line) == RED_LINE_SOUTH


def test_get_names_empty_line():
    line = BetterTrainLine("empty")
    assert names_of(line) == [], "an empty line has no names"


def test_get_names_does_not_change_the_line():
    line = build(RED_LINE_SOUTH)
    names_of(line)
    assert names_of(line) == RED_LINE_SOUTH, \
        "calling get_names should not modify the line"


def test_add_list_matches_manual_add():
    manual = build(RED_LINE_SOUTH)

    via_add_list = BetterTrainLine("test line via add_list")
    via_add_list.add_list(RED_LINE_SOUTH)

    assert names_of(via_add_list) == names_of(manual), \
        "add_list(names) should have the same effect as calling add() once per name"


def test_add_list_empty():
    line = BetterTrainLine("test line")
    line.add_list([])
    assert names_of(line) == []


def test_add_list_extends_existing_line():
    line = build(["Howard"])
    line.add_list(["Jarvis", "Morse"])
    assert names_of(line) == ["Howard", "Jarvis", "Morse"], \
        "add_list should append after whatever is already on the line"


def test_find_middle_station():
    line = build(RED_LINE_SOUTH)
    assert line.find_middle_station().get_name() == "Morse"


def test_find_one_third_station():
    line = build(RED_LINE_SOUTH)
    assert line.find_one_third_station().get_name() == "Jarvis"


def test_find_1_f_station_matches_given_methods():
    line = build(RED_LINE_SOUTH)
    assert line.find_1_f_station(2).get_name() == line.find_middle_station().get_name()
    assert line.find_1_f_station(3).get_name() == line.find_one_third_station().get_name()


def test_find_1_f_station_avoids_size_and_floordiv():
    assert source_avoids(BetterTrainLine.find_1_f_station, ["__size", "//"]), \
        "find_1_f_station should not need self.__size or // -- traversal only"


def test_find_e_f_station_reduces_to_find_1_f_station():
    line = build(RED_LINE_SOUTH)
    for f in [2, 3]:
        assert line.find_e_f_station(1, f).get_name() == line.find_1_f_station(f).get_name(), \
            "find_e_f_station(1, f) must land on the same station as find_1_f_station(f)"


def test_find_e_f_station_general_case():
    line = build(SEVEN_STATIONS)
    # On A-B-C-D-E-F-G: 1/2 -> D, 1/3 -> C, 2/3 -> E. Trace these by
    # hand (same way the README asks you to) if one of these surprises
    # you.
    assert line.find_e_f_station(1, 2).get_name() == "D"
    assert line.find_e_f_station(1, 3).get_name() == "C"
    assert line.find_e_f_station(2, 3).get_name() == "E"


def test_find_e_f_station_avoids_size_and_floordiv():
    assert source_avoids(BetterTrainLine.find_e_f_station, ["__size", "//"]), \
        "find_e_f_station should not need self.__size or // -- traversal only"


TESTS = [
    test_add_single_station,
    test_get_names_on_built_line,
    test_get_names_empty_line,
    test_get_names_does_not_change_the_line,
    test_add_list_matches_manual_add,
    test_add_list_empty,
    test_add_list_extends_existing_line,
    test_find_middle_station,
    test_find_one_third_station,
    test_find_1_f_station_matches_given_methods,
    test_find_1_f_station_avoids_size_and_floordiv,
    test_find_e_f_station_reduces_to_find_1_f_station,
    test_find_e_f_station_general_case,
    test_find_e_f_station_avoids_size_and_floordiv,
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
