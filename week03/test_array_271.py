"""
Simple, plain-Python tests for Array271 (array_271.py).

Still no unittest or pytest -- each test is a function using `assert`
statements. All tests go through the class's public accessors
(`get_capacity()`, `get_item()`, etc.) rather than reaching into private
attributes like `_capacity` directly -- that's the same encapsulation
rule the class itself follows, applied to the tests that exercise it.

How to run this file:
    python3 test_array_271.py

The first several tests exercise what's already built and working:
construction, `add`/`_resize`, `get_item`, and `__str__`. The last two
tests, `test_remove_returns_item` and `test_remove_shifts_and_resizes_down`,
are checkpoints for THIS WEEK'S assignment -- they are EXPECTED TO FAIL
until you make the two modifications to `remove` described in README.md.
"""

from array_271 import Array271


def test_default_construction():
    """A freshly constructed array should use the default capacity (2)
    and resize_factor (0.25), start empty, and pre-fill its storage with
    None placeholders."""
    arr = Array271()

    assert arr.get_capacity() == 2, "default capacity should be 2"
    assert arr.get_resize_factor() == 0.25, "default resize_factor should be 0.25"
    assert arr.get_occupancy() == 0, "a brand-new array should start with occupancy 0"
    assert arr.get_items() == [None, None], "items should be pre-sized to capacity, all None"

    print("ok: test_default_construction")


def test_custom_construction():
    """The constructor should honor whatever capacity and resize_factor
    are passed in, instead of always using the defaults."""
    arr = Array271(capacity=5, resize_factor=0.5)

    assert arr.get_capacity() == 5
    assert arr.get_resize_factor() == 0.5
    assert arr.get_occupancy() == 0
    assert arr.get_items() == [None, None, None, None, None]

    print("ok: test_custom_construction")


def test_add_single_item_without_resizing():
    """Adding one string to an array that has room should not need to
    resize at all -- it should just occupy the next free slot and bump
    occupancy by one."""
    arr = Array271(capacity=3, resize_factor=0.25)

    arr.add("Mississippi")

    assert arr.get_occupancy() == 1, "occupancy should go up by 1 after one add"
    assert arr.get_capacity() == 3, "capacity should be unchanged -- there was room"
    assert arr.get_item(0) == "Mississippi", "the new string should land in slot 0"
    assert arr.get_item(1) is None, "unused slots should still be None"
    assert arr.get_item(2) is None, "unused slots should still be None"

    print("ok: test_add_single_item_without_resizing")


def test_add_multiple_items_fills_slots_in_order():
    """Repeated adds should fill slots left to right, in the order the
    strings were added, without disturbing earlier entries."""
    arr = Array271(capacity=4, resize_factor=0.25)

    arr.add("M")
    arr.add("i")
    arr.add("s")

    assert arr.get_occupancy() == 3
    assert arr.get_item(0) == "M"
    assert arr.get_item(1) == "i"
    assert arr.get_item(2) == "s"
    assert arr.get_item(3) is None

    print("ok: test_add_multiple_items_fills_slots_in_order")


def test_add_triggers_resize():
    """With the default capacity of 2, adding a THIRD string forces the
    array to grow: `add` notices occupancy == capacity and calls
    `_resize()`. `_resize` is already implemented, so this should pass:
    capacity grows past 2, and all three strings remain present, in
    order."""
    arr = Array271()  # capacity=2, resize_factor=0.25

    arr.add("this")
    arr.add("is")
    arr.add("full")  # this add triggers a resize

    assert arr.get_capacity() > 2, "capacity should have grown past the original 2"
    assert arr.get_occupancy() == 3, "occupancy should be 3 after three successful adds"
    assert arr.get_item(0) == "this"
    assert arr.get_item(1) == "is"
    assert arr.get_item(2) == "full"

    print("ok: test_add_triggers_resize")


def test_get_item_out_of_range_returns_none():
    """A negative index, or an index at/past occupancy, should return
    None instead of raising an IndexError -- even if that index is still
    within capacity."""
    arr = Array271(capacity=3, resize_factor=0.25)
    arr.add("kale")

    assert arr.get_item(-1) is None, "a negative index should return None"
    assert arr.get_item(1) is None, "an index within capacity but past occupancy should return None"
    assert arr.get_item(99) is None, "a wildly out-of-range index should return None"

    print("ok: test_get_item_out_of_range_returns_none")


def test_str_shows_occupied_items_only():
    """__str__ should mention capacity and occupancy, and list only the
    occupied slots -- not the trailing Nones."""
    arr = Array271(capacity=3, resize_factor=0.25)
    arr.add("turnip")

    text = str(arr)

    assert "turnip" in text, "the occupied item should appear in the string"
    assert "None" not in text, "unoccupied trailing slots should not appear"

    print("ok: test_str_shows_occupied_items_only")


def test_remove_invalid_index_does_not_crash():
    """Removing an index outside the occupied range should fail
    gracefully -- no exception -- and leave the array untouched. This
    holds both before and after this week's assignment, so it isn't a
    checkpoint test; it's a baseline that should keep passing throughout.
    """
    arr = Array271(capacity=3, resize_factor=0.25)
    arr.add("kale")

    result = arr.remove(5)

    assert not result, "an out-of-range index should not report success"
    assert arr.get_occupancy() == 1, "a failed remove should not change occupancy"

    print("ok: test_remove_invalid_index_does_not_crash")


def test_remove_returns_item():
    """CHECKPOINT 1 for this week's assignment: `remove` should return
    the removed string itself, not a True/False success flag.

    EXPECTED TO FAIL until you make modification #1 in README.md."""
    arr = Array271(capacity=3, resize_factor=0.25)
    arr.add("kale")
    arr.add("turnip")

    removed = arr.remove(0)

    assert removed == "kale", "remove(0) should return the string that was removed"

    print("ok: test_remove_returns_item")


def test_remove_shifts_and_resizes_down():
    """CHECKPOINT 2 for this week's assignment: after removing an item,
    later items should shift down to close the hole, occupancy should
    decrease, and once usage drops low enough the array should shrink.

    EXPECTED TO FAIL until you make modification #2 in README.md."""
    arr = Array271(capacity=4, resize_factor=0.25)
    arr.add("kale")
    arr.add("turnip")
    arr.add("eggplant")

    arr.remove(0)

    assert arr.get_occupancy() == 2, "occupancy should decrease after a successful remove"
    assert arr.get_item(0) == "turnip", "later items should shift down to fill the hole"
    assert arr.get_item(1) == "eggplant"

    print("ok: test_remove_shifts_and_resizes_down")


if __name__ == "__main__":
    test_default_construction()
    test_custom_construction()
    test_add_single_item_without_resizing()
    test_add_multiple_items_fills_slots_in_order()
    test_add_triggers_resize()
    test_get_item_out_of_range_returns_none()
    test_str_shows_occupied_items_only()
    test_remove_invalid_index_does_not_crash()
    test_remove_returns_item()
    test_remove_shifts_and_resizes_down()

    print("\nAll tests passed.")
