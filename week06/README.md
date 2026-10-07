# Week 6 Assignment: Generalizing the Fast/Slow Sweep Again, Plus `add_list` and `get_names`

## The task

In class we wrote two methods on `BetterTrainLine`, both using the same
fast/slow trick: `find_middle_station` (fast moves 2 stations per
iteration) and `find_one_third_station` (fast moves 3). Then
`find_1_f_station(f)` made those two a special case of one idea: land on
the station 1/f of the way down the line, for whatever `f` you're given.

This week you write three methods: one that makes building a line less
repetitive, one that turns a line back into something you can print,
loop over, or compare at a glance, and one that generalizes
`find_1_f_station` one step further.

`BetterTrainLine` is, structurally, a singly linked list — `Station` is
the node, `get_next` is the link. If you want the bigger picture behind
that pattern, Wikipedia has
[a solid overview of linked lists' history and variants](https://en.wikipedia.org/wiki/Linked_list).
Note that any code shown there will unfortunately be in C++, not
Python — read it for the ideas and structure, not the syntax.

## What you're given

- `better_train_line_271.py` — the scaffold. `__init__`, `__str__`,
  `add`, `find_middle_station`, `find_one_third_station`, and
  `find_1_f_station` are all complete and unchanged from class.
  `add_list`, `get_names`, and `find_e_f_station` are `TODO`.
- `Station.py` — unchanged from class.
- `test_better_train_line_271.py` — plain-`assert` tests for all three
  methods you're writing, no testing framework required. Everything
  except the `find_e_f_station` checks should already pass against the
  given scaffold; those fail (or crash with `AttributeError`) until you
  implement it. Run it as you work:

  ```
  python3 test_better_train_line_271.py
  ```

Run the scaffold directly to see the given methods work:

```
python3 better_train_line_271.py
```

## What you need to do

### 1. `add_list(names)`

Every line built so far has been built one `add` call per station. Write
`add_list(self, names:list[strR])` so it takes a list of strings and adds one station per
name, in order — `add_list(["Howard", "Jarvis", "Morse"])` should have
the exact same effect as calling `add` three times in a row, one for each station.

- Don't duplicate `add`'s head/last-pointer logic. Build each `Station`
  and hand it to `self.add(...)`.

### 2. `get_names()`

Write `get_names()` so it walks the whole line, head to last, and
returns a list of every station's name, in the order you visited them —
`get_names()` on `Howard -> Jarvis -> Morse` returns
`["Howard", "Jarvis", "Morse"]`.

- This is the same traversal shape you've used all along (start at the
  head, move with `get_next()`, stop when `has_next()` is false) — the
  only difference is you're visiting every station instead of skipping
  ahead, and collecting a name at each stop instead of searching for
  one.

### 3. `find_e_f_station(e, f)`

Write the method that makes `find_1_f_station` a special case of one
more-general idea: `find_e_f_station(e, f)` finds the station `e` out of
every `f` stations down the line. `find_e_f_station(1, 2)` should land
on the same station as `find_1_f_station(2)` (and `find_middle_station`);
`find_e_f_station(1, 3)` should land on the same station as
`find_1_f_station(3)` (and `find_one_third_station`).

**The catch:** same as last week — you may not use `self.__size` or `//`
anywhere in this method. The traversal is still the whole point.

- Use the same `slow`/`fast` pattern as `find_1_f_station`, but now
  scale *both* sides of it: `slow` advances `e` stations per iteration;
  `fast` advances `f` stations per iteration.
- Stop with the same idea as before: as soon as `fast` can't complete
  one more full `f`-station hop.
- You can assume `e` and `f` are positive integers with `e < f`; no need
  to validate them or handle an empty line for this assignment.
- Check your work against the methods you already have: on
  `Howard -> Jarvis -> Morse -> Loyola -> Granville`,
  `find_e_f_station(1, 2)` should print `Morse` and `find_e_f_station(1, 3)`
  should print `Jarvis` — both must match `find_1_f_station` exactly,
  since `e = 1` is the same case. Then trace `find_e_f_station(2, 3)` by
  hand on the same line, both by counting 2/3 of the way down from the
  head and 1/3 of the way up from the last station, and confirm your
  method lands where you expect.

**Rules, same as class:** one `return` per method; no `break`; talk to a
`Station` only through its methods (`get_name`, `get_next`, `has_next`,
`set_next`), never its private fields; do not change `Station.py`, the
given methods, or any method signature.

## Questions to be ready to discuss in class

- `add_list` could walk `names` and call `self.add(...)` each time, or
  it could try to reuse `__last` directly without going through `add`.
  Why is going through `add` the safer choice, even though it's "one
  more function call" per station?
- `get_names()` and `__str__` both turn a line into something printable,
  but `__str__` doesn't call `get_names()`. Would it make sense for it
  to? What would change about what gets printed?
- `find_e_f_station(1, f)` has to behave identically to
  `find_1_f_station(f)` — not just "usually," but always. Why does that
  follow just from the shape of the method, without tracing through
  examples?
- Where do `e` and `f` each appear in your loop, and what would change
  about which station you land on if you swapped them?
- "2/3 of the way down" and "1/3 of the way up from the end" describe
  the same fraction of the line, but `find_e_f_station` only ever walks
  from the head. Did they land on the same station on your traced
  example? If a case like this doesn't line up exactly, why not?
- Why doesn't `find_e_f_station` need `self.__size` any more than
  `find_1_f_station` did? What would you have to do differently if you
  *did* want to use it?
- `find_middle_station`, `find_one_third_station`, and `find_1_f_station`
  could now all be rewritten as one-line calls to `find_e_f_station`.
  What's gained — and what, if anything, is lost — by actually deleting
  them in favor of the fully general version?

## How to submit

Submit your completed `better_train_line_271.py`. Confirm it still prints
correctly with:

```
python3 better_train_line_271.py
```

and that it passes the provided tests with:

```
python3 test_better_train_line_271.py
```

Due **Friday, October 9**, via Sakai.
