# Week 4 Assignment: `TwoDimensional` — A Grid That Honors the Contract

## Background

This week we stepped back from `Array271` and asked what every data
structure we build should promise. The answer is `OurContract`: `add`,
`contains`, `index_of`, `indices`, and `count`. Python enforces only that
those methods *exist* — the docstrings in `OurContract.py` say what they
must *do*, and keeping to that is on you.

`Array271` is one structure that keeps that promise. This assignment asks
you to write a second, built very differently, so you can see what the
contract buys you: the same five methods, a completely different shape
underneath.

## The data structure

`TwoDimensional` stores strings in a grid of rows and columns, like a
spreadsheet.

- **Rows** are labeled with numbers, starting at `1`.
- **Columns** are labeled with letters, starting at `'A'`. To avoid
  confusion, the letters **I, O, and Z are never used** — they look too
  much like the digits 1, 0, and 2 or 7. That leaves 23 letters:

  ```
  A B C D E F G H J K L M N P Q R S T U V W X Y
  ```

- When a grid has more than 23 columns, labels continue with **double
  letters** built from the same 23 letters, the first letter changing
  slowest: `AA`, `AB`, …, `AY`, `BA`, `BB`, …, `YY`. Your class supports
  at most 23 + 23 × 23 = **552 columns**.

Strings are added **row-major**:

```
first string   -> row 1, column A
second string  -> row 1, column B
...
(when row 1 is full) -> row 2, column A
```

The number of **columns is fixed** when the object is created (default
4). The number of **rows starts at 2 and grows on demand**: when the grid
is full and another string arrives, add one more row. 

Positions are reported as **(row, column label) pairs**, e.g. `(1, 'B')`
or `(3, 'AA')`.

## What you're given

- `two_dimensional.py` — a scaffold. The class header, constants, and
  constructor are complete; the getters `get_columns`, `get_rows`, and
  `get_occupancy` are given; every other method is a `TODO`.
- `OurContract.py` — the contract, in `week04/`.
- `test_two_dimensional.py` — run it with:

  ```
  python3 test_two_dimensional.py
  ```

  Four of the 16 tests pass against the scaffold as-is. When your
  implementation is correct, all 16 pass and the last line prints
  `All tests passed.`

## What you need to do

Complete these in `two_dimensional.py`:

1. **`__column_label(c)`** — turn a 0-based column number into its label:
   `0 → 'A'`, `8 → 'J'` (no `I`), `22 → 'Y'`, `23 → 'AA'`, `551 → 'YY'`.
   Use `COLUMN_LETTERS` and do the arithmetic; do not type out 552
   labels.
2. **`__position(p)`** — turn a flat list index into a `(row, label)`
   pair. The grid is stored in one flat list in row-major order, so with
   4 columns, index 5 is row 2, column `'B'`.
3. **`__grow()`** — add one more row: allocate a bigger list, copy the old
   items over, swap it in, and update the row count. (Same three steps as
   `resize` in Week 2.)
4. **`add(value)`** — grow first if the grid is full, then store the
   string in the next free cell.
5. **`index_of(value)`** — the `(row, label)` pair of the **first** match,
   or an empty tuple `()` if there is none. (`OurContract` says an
   `index_of` position is an integer; for a grid, a position is a pair.)
   Search only the cells that hold strings. As discussed in class, a list
   in place of a tuple (`[]` for "none") is equally acceptable.
6. **`indices(value)`** — a tuple of the pair for **every** match in
   row-major order, e.g. `((1, 'B'), (3, 'A'))`, or `()` if there is none.
   A single match is still a tuple: `((2, 'C'),)`. A list of pairs
   (`[(1, 'B'), (3, 'A')]`, `[]`, `[(2, 'C')]`) is equally acceptable —
   what matters is a sequence of pairs, not one flat run of rows and labels.
7. **`contains(value)`** — delegate to `index_of`, as we did in class.
8. **`count(value)`** — how many cells hold `value`.

The constructor's fallback is already written: a column count below 1 or
above 552 quietly becomes the default of 4 rather than crashing.

**Imports:** it is OK to import anything from the following modules, and
nothing else:

- [`abc`](https://docs.python.org/3/library/abc.html)
- [`typing`](https://docs.python.org/3/library/typing.html)
- [`__future__`](https://docs.python.org/3/library/__future__.html)
- `OurContract` — the contract we wrote for 271

**Rules, same as class:** one `return` per method (build up a result
variable); no `break`; no other imports; no magic numbers —
use `DEFAULT_COLUMNS`, `INITIAL_ROWS`, `MAX_COLUMNS`, and
`COLUMN_LETTERS`. Do not change any method signature.

## Questions to be ready to discuss in class

- Why does one flat list holding the whole grid make `add` simple? What
  would `add` look like with a list of lists instead?
- How do you get from a flat index to a row and a column, and why does
  `//` matter here?
- Why must `index_of` search only the occupied cells? What would go wrong
  searching all `rows × columns` cells?
- `index_of` and `indices` may return tuples or lists. Whichever you chose,
  why does a "not found" answer and a one-match answer still have to be a
  sequence of the right shape? What are the trade-offs of a tuple versus a
  list here?
- `Array271` and `TwoDimensional` share no code, yet both are a
  `OurContract`. What does someone using either one get to assume?
- Growing by one row each time is easy to write. What does it cost when a
  million strings arrive? What might you do differently?

## How to submit

Submit your completed `two_dimensional.py` and confirm
`python3 test_two_dimensional.py` prints `All tests passed.` at the end.
Due **Friday, September 25** at the start of class, via Sakai.

## Reading

New this week:

- Magic methods — [Introducing Python, 3rd edition, Ch. 11 ("Objects"),
  the "Magic Methods" section](https://learning.oreilly.com/library/view/introducing-python-3rd/9781098174392/ch11.html#c11_h_magic_methods)
- Abstract base classes — [Python documentation, `abc` — Abstract Base
  Classes](https://docs.python.org/3/library/abc.html)

Continue with the earlier reading too —
[Think Python, 3rd edition](https://allendowney.github.io/ThinkPython/),
Ch. 9 ("Lists") and Ch. 16 ("Classes and Objects"), and [Introducing
Python, 3rd edition](https://learning.oreilly.com/library/view/introducing-python-3rd/9781098174392/),
Ch. 8 ("Tuples and Lists") and Ch. 11 ("Objects").
