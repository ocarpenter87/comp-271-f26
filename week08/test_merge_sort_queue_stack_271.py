"""
Plain-assert tests for Week 8: merge_sort_iterative, ArrayQueue271,
ArrayStack271 (merge_sort_queue_stack_271.py).

No testing framework -- each test is a function with `assert` statements.

How to run this file:
    python test_merge_sort_queue_stack_271.py

Everything for a part fails (or raises) until you implement it. Work one
part at a time; the output tells you which checks pass.
"""

import inspect
import random

from merge_sort_queue_stack_271 import (
    merge_sort, merge_sort_iterative, ArrayQueue271, ArrayStack271,
)


# ---------------------------------------------------------------- Part 1

def test_iterative_empty_and_single():
    assert merge_sort_iterative([]) == [], "empty list sorts to empty list"
    assert merge_sort_iterative([7]) == [7], "one element is already sorted"


def test_iterative_power_of_two_length():
    assert merge_sort_iterative([7, 6, 5, 4, 3, 2, 1, 0]) == [0, 1, 2, 3, 4, 5, 6, 7]


def test_iterative_odd_lengths():
    # The leftover run at the end of a pass has no partner (or a short one).
    assert merge_sort_iterative([3, 1, 2]) == [1, 2, 3], "length 3"
    assert merge_sort_iterative([5, 4, 3, 2, 1]) == [1, 2, 3, 4, 5], "length 5"
    assert merge_sort_iterative([9, 8, 7, 6, 5, 4, 3, 2, 1]) == list(range(1, 10)), "length 9"


def test_iterative_duplicates_and_sorted_input():
    assert merge_sort_iterative([2, 1, 2, 1, 2]) == [1, 1, 2, 2, 2]
    assert merge_sort_iterative([1, 2, 3, 4]) == [1, 2, 3, 4]


def test_iterative_does_not_modify_input():
    original = [4, 3, 2, 1]
    merge_sort_iterative(original)
    assert original == [4, 3, 2, 1], "the input list must be left unchanged"


def test_iterative_matches_recursive_on_random_data():
    for n in range(0, 40):
        data = [random.randint(0, 50) for _ in range(n)]
        assert merge_sort_iterative(data) == merge_sort(data) == sorted(data), \
            f"disagreement on {data}"


def test_iterative_is_really_iterative():
    source = inspect.getsource(merge_sort_iterative)
    assert source.count("merge_sort_iterative(") == 1, \
        "merge_sort_iterative must not call itself (only its def line may name it)"
    assert "merge_sort(" not in source.replace("merge_sort_iterative(", ""), \
        "merge_sort_iterative must not call the recursive merge_sort either"
    assert "sorted(" not in source and ".sort(" not in source, \
        "no built-in sorting"


# ---------------------------------------------------------------- Part 2: queue

def test_queue_starts_empty():
    q = ArrayQueue271()
    assert len(q) == 0 and q.is_empty() and not q.is_full()
    assert q.remove() is None, "removing from an empty queue fails quietly with None"


def test_queue_is_fifo():
    q = ArrayQueue271()
    for x in "ABC":
        assert q.add(x) is True
    assert len(q) == 3
    assert [q.remove(), q.remove(), q.remove()] == ["A", "B", "C"]
    assert q.is_empty()


def test_queue_refuses_when_full():
    q = ArrayQueue271()
    for x in range(4):
        assert q.add(x) is True
    assert q.is_full() and len(q) == 4
    assert q.add(99) is False, "a full queue refuses new items"
    assert len(q) == 4
    assert q.remove() == 0, "the refused item must not have overwritten anything"


def test_queue_pointer_rules():
    q = ArrayQueue271()
    assert (q.front, q.back) == (0, 0), "front and back start at the same place"
    q.add("A")
    assert (q.front, q.back) == (0, 1), "adding moves only back"
    q.add("B")
    q.remove()
    assert (q.front, q.back) == (1, 2), "removing moves only front"


def test_queue_wraps_around():
    q = ArrayQueue271()
    for x in "ABCD":
        q.add(x)
    assert q.remove() == "A"
    assert q.remove() == "B"
    assert q.add("E") is True and q.add("F") is True
    assert q.back == 2, "back wrapped from index 3 around to 0 and then 1 -> 2"
    assert q.is_full()
    assert q.storage[0] == "E" and q.storage[1] == "F", "new items reuse the freed front slots"
    assert [q.remove() for _ in range(4)] == ["C", "D", "E", "F"], "order survives the wrap"
    assert q.is_empty() and q.front == q.back == 2


def test_queue_full_and_empty_both_have_front_equal_back():
    q = ArrayQueue271()
    for x in range(4):
        q.add(x)
    assert q.front == q.back and q.is_full() and not q.is_empty()
    for _ in range(4):
        q.remove()
    assert q.front == q.back and q.is_empty() and not q.is_full()


def test_queue_long_run_of_wraps():
    q = ArrayQueue271()
    expected = []
    for step in range(100):
        q.add(step)
        expected.append(step)
        if len(expected) > 2:
            assert q.remove() == expected.pop(0)
    assert len(q) == 2


def test_queue_other_capacity():
    q = ArrayQueue271(capacity=3)
    for x in range(3):
        q.add(x)
    assert q.add(3) is False
    assert q.remove() == 0 and q.add(3) is True and q.back == 1


# ---------------------------------------------------------------- Part 2: stack

def test_stack_starts_empty():
    s = ArrayStack271()
    assert len(s) == 0 and s.is_empty() and not s.is_full()
    assert s.top == 3, "an empty stack's top starts at capacity - 1"
    assert s.remove() is None, "removing from an empty stack fails quietly with None"


def test_stack_is_lifo():
    s = ArrayStack271()
    for x in "ABC":
        assert s.add(x) is True
    assert [s.remove(), s.remove(), s.remove()] == ["C", "B", "A"]
    assert s.is_empty()


def test_stack_fills_from_the_back():
    s = ArrayStack271()
    s.add("A")
    s.add("B")
    assert s.storage[3] == "A" and s.storage[2] == "B"
    assert s.top == 1, "top is where the next item will go"


def test_stack_refuses_when_full():
    s = ArrayStack271()
    for x in range(4):
        assert s.add(x) is True
    assert s.is_full()
    assert s.add(99) is False
    assert s.remove() == 3, "the refused item must not have overwritten anything"


def test_stack_interleaved():
    s = ArrayStack271()
    s.add(1)
    s.add(2)
    assert s.remove() == 2
    s.add(3)
    s.add(4)
    assert [s.remove(), s.remove(), s.remove()] == [4, 3, 1]
    assert s.remove() is None and s.top == 3


def test_stack_slot_cleared_after_remove():
    s = ArrayStack271()
    s.add("A")
    s.remove()
    assert s.storage == [None, None, None, None], "removed slots go back to None"


if __name__ == "__main__":
    tests = [(name, fn) for name, fn in sorted(globals().items())
             if name.startswith("test_") and callable(fn)]
    passed = 0
    for name, fn in tests:
        try:
            fn()
            print(f"ok    {name}")
            passed += 1
        except Exception as err:   # AssertionError, NotImplemented, TypeError...
            print(f"FAIL  {name}: {type(err).__name__}: {err}")
    print(f"\n{passed} of {len(tests)} checks passed")
