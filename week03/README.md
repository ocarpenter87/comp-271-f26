# Week 3 Assignment: `Array271` — Removing Items Properly

## Background

Wednesday's class picked up `Array271` where the Week 2 assignment left
off: you had already written `resize`, so we used that as a springboard
into object design — what `self` actually means, the difference between
an object attribute (`self._capacity`) and a local variable inside a
method (`growth`, `temp`), and why every field should be private with
accessor ("getter") methods as the only sanctioned way in. `add` is
user-facing; `_resize` is internal and should never be called directly —
the array resizes itself when it needs to, not on demand.

Friday we reviewed that architecture, added `__str__` so printing an
array shows something useful instead of a memory address, tightened
`get_item` so an out-of-range index returns `None` instead of crashing,
wrote `remove(i)` together (bounds-check, clear the slot, report
success), and talked about the difference between a single leading
underscore (`_resize` — a convention, easy to violate) and a double
leading underscore (name-mangled by Python — harder to reach from
outside the class by accident).

That `remove` has two problems, on purpose. This assignment fixes them —
and, along the way, retires `_resize` in favor of two more clearly named,
more clearly private methods.

## What you're given

`array_271.py`, the class as built in class through Friday: `__init__`,
`__str__`, the getters (including the bounds-checked `get_item`), `add`,
`_resize`, and the current `remove`. Read `remove`'s docstring in the
file — it spells out exactly what's wrong with it, which is also this
assignment.

Also given: `test_array_271.py`. Run it with:

```
python3 test_array_271.py
```

Eight of the ten tests already pass against the file as-is. The last two,
`test_remove_returns_item` and `test_remove_shifts_and_resizes_down`, are
your checkpoints — they currently fail. When your implementation is
correct, all ten should pass. (All ten tests go through the public
getters, never `_resize` directly, so the rename below won't break any of
them.)

## What you need to do

Modify `Array271` so that it makes **all three** of these changes:

1. **Return the removed item, not a success flag.** Right now `remove`
   returns `True`/`False`. Change it to return the string that was at
   index `i` — and think about what it should return when `i` is
   invalid, so a caller can still tell success from failure without a
   separate boolean (hint: `None` is not a valid string, so it doubles as
   "nothing was removed" — but be ready to explain that choice).
2. **Close the hole.** After removing the item at index `i`, shift every
   item after it down by one position, then decrement `occupancy`. This
   keeps occupied slots contiguous starting at index 0, which `add`
   depends on — right now, removing an item from the middle leaves a
   `None` gap that `add` will never fill, because `add` always writes to
   `items[occupancy]`.
3. **Set `_resize` aside, and split it into `__upsize()` and
   `__downsize()`.** Rename `_resize` to `__upsize()` — same job, same
   logic (grow capacity by `resize_factor`, copy the occupied items into
   a bigger list), just a name that says what it actually does, and a
   double leading underscore so Python name-mangles it, the way we
   discussed in class. `add` should call `__upsize()` exactly where it
   used to call `_resize()`.

   Then write a new `__downsize()` method alongside it: same shape as
   `__upsize` — allocate a new list, copy the occupied items over, swap
   it in — but shrinking capacity instead of growing it. Call
   `__downsize()` from `remove`, once occupancy drops low enough relative
   to capacity (roughly below 50% usage — we'll pin down the exact
   threshold in class).

   Keep growing and shrinking as two separate methods rather than one
   method that branches — `__upsize` and `__downsize` should each do one
   job.

Do not change the signature or behavior of `__init__`, `__str__`,
`get_item`, or the other getters. `add`'s only change is the one-line
swap of `_resize()` for `__upsize()`.

## Questions to be ready to discuss in class

- What should `remove` return when `i` is invalid, and why does that
  choice matter to a caller who wants to distinguish "nothing was there"
  from "something was there and it was empty"?
- Why must the shift happen *before* `occupancy` is decremented, not
  after?
- What threshold should trigger a call to `__downsize`, and why doesn't
  it have to be the exact mirror of the growth threshold? What happens if
  you shrink too aggressively right after `__upsize` just grew the array?
- Should there be a floor on how small `capacity` can ever get — could a
  bad `__downsize` formula ever bring capacity down to 0 or below
  occupancy?
- Now that `__upsize` and `__downsize` are name-mangled instead of just
  single-underscore, what would it actually take to call one from outside
  the class? Why is that a meaningfully different guarantee than the
  single-underscore convention `_resize` relied on?

## How to submit

Submit your completed `array_271.py` (with `remove` returning the removed
item and shifting/shrinking correctly, and `_resize` replaced by
`__upsize`/`__downsize`) and confirm `python3 test_array_271.py` prints
`All tests passed.` at the end.

## Reading

No new reading was assigned in class this week. Continue with the Week 2
reading if you haven't finished it — [Think Python, 3rd edition](https://allendowney.github.io/ThinkPython/),
Ch. 9 ("Lists") and Ch. 16 ("Classes and Objects"), and [Introducing
Python, 3rd edition](https://learning.oreilly.com/library/view/introducing-python-3rd/9781098174392/),
Ch. 8 ("Tuples and Lists") and Ch. 11 ("Objects").
