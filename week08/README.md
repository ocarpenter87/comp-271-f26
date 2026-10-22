# Week 8 Assignment — Merge Sort Without Recursion, and a Queue and Stack on a Plain Array

## The task

This week has two parts that look unrelated and turn out to be about the
same thing: **where pending work lives.**

- **Part 1.** In class we wrote merge sort recursively, and the call
  stack quietly kept track of every half-finished sort. You will rewrite
  it *without recursion*, so that nothing is left to keep track of for
  you, and then explain in writing what your version does and why it
  works.
- **Part 2.** On Friday we said that a stack and a queue are not data
  structures but *rules about which item comes out next*. You will make
  that concrete by building both on top of the same thing: a plain,
  fixed-capacity array.

## What you're given

- `merge_sort_queue_stack_271.py` — the scaffold.
  - `merge` and the recursive `merge_sort` are complete (the version from
    class, with the print statements removed).
  - `merge_sort_iterative` is `TODO` (Part 1).
  - `ArrayQueue271` and `ArrayStack271` each have a finished constructor,
    `__len__`, `is_empty`, `is_full` and `__str__`. Their `add` and
    `remove` methods are `TODO` (Part 2).
- `test_merge_sort_queue_stack_271.py` — plain-`assert` tests, no
  testing framework. Run it as you work:

  ```
  python3 test_merge_sort_queue_stack_271.py
  ```

  Each test prints `ok` or `FAIL` with a reason, so you can work one part
  at a time. A few checks pass on the untouched scaffold (an empty list,
  an empty queue); the rest fail until you write the code.

As always, every function and method has **exactly one `return`**: set a
result variable to the "didn't work" value first, and overwrite it only
once the guard condition passes. Write your own extra `assert`s for any
case you're unsure about before trusting a printed result.

---

## Part 1 — Iterative merge sort, and an explanation

### The code

Write `merge_sort_iterative(arr)`. It must:

- return a **new** sorted list and leave `arr` unchanged;
- use the given `merge` for the merging itself;
- contain **no recursion** — it may not call itself or `merge_sort` — and
  no `sorted()` or `.sort()`;
- work for every length, including 0, 1, odd lengths, and lists with
  repeated values.

**A way in.** Think about the recursive version's call tree, but read it
from the bottom up. The recursion bottoms out at lists of length 1,
because a single element is trivially sorted. Rather than splitting a list
down to those pieces, *start* from them: view the list as a row of sorted
runs of width 1, merge neighboring pairs into sorted runs of width 2, then
merge neighboring pairs of those, and so on. Three things need settling
before you code: what the loop's control variable is, what makes the loop
stop, and what happens at the right-hand end when a run has no partner (or
only a short one).

### The explanation

Alongside the code, submit a short file (plain text is fine)
(roughly a page — shorter is fine if it is clear), written in your own
words. Do not paste your code in as the explanation; the code is already
submitted. Answer these:

1. **What does your function do, in plain language?** Describe one pass of
   the outer loop as if to a classmate who has not seen your code.
2. **Trace it.** Show the list after each pass for
   `[5, 2, 4, 7, 1, 3, 2, 6, 9]`, marking where the runs begin and end.
   (Nine elements is on purpose.)
3. **The odd leftover.** In your trace, what happened to the `9`? Explain
   how your code handles a run that has no partner, and why it is correct
   to do so.
4. **Why does it stop, and why is the result sorted?** Say what is true of
   the list at the end of every pass, and how that fact guarantees the
   final answer.
5. **Where did the call stack go?** The recursive version used the call
   stack to remember pending work. In your version, what plays that role —
   what is "remembered," and where?

---

## Part 2 — A queue and a stack on a plain array

Both classes store their items in `self.storage`, a Python list created
once with `capacity` slots (default 4) and **never resized, never
appended to, never `.pop()`ed**. You are only ever assigning to
`storage[i]` for a chosen `i`. When the structure is full it simply
refuses; it does not grow, unlike the dynamic array.

Both classes also track `used`, the number of items currently stored. It
is the single source of truth for "empty" and "full" (see the warning in
the queue section for why).

Both classes use the same two operations and the same *quiet-failure*
convention as the earlier contract work:

| Method | Success | Failure (nothing changes) |
|---|---|---|
| `add(item)` | stores the item, returns `True` | structure is full → returns `False` |
| `remove()` | returns the item that comes out next, and puts `None` back in its slot | structure is empty → returns `None` |

What differs is *which* item comes out, and that comes entirely from how
the pointers move.

### The stack, `ArrayStack271`

As in class, the stack is filled from the **back** of the array toward the
front. One pointer is enough:

- `top` is the index where the **next item will be written**. A new, empty
  stack has `top = capacity - 1`.
- `add` writes to `storage[top]`, then moves `top` one step toward 0.
- `remove` moves `top` one step back the other way, then reads (and
  clears) the item now sitting at `storage[top]`.

A trace, capacity 4 (`_` is `None`):

| Step | `storage` | `top` | `used` | Returns |
|---|---|---|---|---|
| new | `[_, _, _, _]` | 3 | 0 | |
| `add("A")` | `[_, _, _, A]` | 2 | 1 | `True` |
| `add("B")` | `[_, _, B, A]` | 1 | 2 | `True` |
| `remove()` | `[_, _, _, A]` | 2 | 1 | `"B"` |
| `remove()` | `[_, _, _, _]` | 3 | 0 | `"A"` |
| `remove()` | `[_, _, _, _]` | 3 | 0 | `None` |

Notice the stack never needs to wrap: its pointer only slides up and down
one end. **Warning:** when the stack is completely full, `top` is `-1`,
and in Python `storage[-1]` is a perfectly legal index — it is the *last*
slot. Writing there would silently destroy your oldest item rather than
raising an error. Always ask `is_full()` first.

### The queue, `ArrayQueue271`

A queue removes from one end and adds at the other, so it needs two
pointers:

- `front` — index of the **next item to remove**.
- `back` — index where the **next item will be written**.
- Both start at 0. `front` moves **only** when you remove; `back` moves
  **only** when you add.

Class showed the shifting version: always remove from index 0 and slide
every other item left. It is correct, but every `remove` costs time
proportional to the number of items. The pointer version never moves an
item. Instead the pointers move, and when one reaches the end of the
array it **wraps around** to the start. That is what `%` is for:

```python
self.back = (self.back + 1) % self.capacity
```

For capacity 4, `(3 + 1) % 4` is `0`, and every other value is just
`+ 1`. No `if` statement to test for "past the end" is needed — the clock
does it: after 12 comes 1, not 13.

A trace, capacity 4:

| Step | `storage` | `front` | `back` | `used` | Returns |
|---|---|---|---|---|---|
| new | `[_, _, _, _]` | 0 | 0 | 0 | |
| `add("A")` | `[A, _, _, _]` | 0 | 1 | 1 | `True` |
| `add("B")` | `[A, B, _, _]` | 0 | 2 | 2 | `True` |
| `add("C")` | `[A, B, C, _]` | 0 | 3 | 3 | `True` |
| `remove()` | `[_, B, C, _]` | 1 | 3 | 2 | `"A"` |
| `add("D")` | `[_, B, C, D]` | 1 | **0** | 3 | `True` |
| `add("E")` | `[E, B, C, D]` | 1 | 1 | 4 | `True` |
| `add("F")` | `[E, B, C, D]` | 1 | 1 | 4 | `False` |
| `remove()` | `[E, _, C, D]` | 2 | 1 | 3 | `"B"` |

Look at the row for `add("D")`: `back` wrapped from 3 to 0, and `E` landed
in the slot that `A` freed. The items are no longer in order *in the
array*, but they are in order *in the queue*: the next to leave is the one
at `front`, then `front + 1`, wrapping the same way.

**Warning — full looks like empty.** In the row for `add("E")`, the queue
is completely full and `front == back == 1`. At the very start, the queue
is completely empty and `front == back == 0`. The pointers alone cannot
tell these apart. That is the reason both classes carry `used`: `is_empty`
and `is_full` compare `used` against 0 and `capacity`, and your `add` and
`remove` must keep `used` correct.

### What each method should do

For each of the four methods, in your own words before you code: which
pointer moves, in which direction, and does it wrap? Which of `used`,
`storage` change? What is the guard condition, and what is the
pessimistic default value you set before checking it?

The tests include a few things worth predicting before you run them:
a queue that wraps around many more times than its capacity, a refused
`add` that must not overwrite anything, and a `remove` that must leave
`None` behind in the slot it emptied.

---

## What to submit

- Your completed scaffold, `merge_sort_queue_stack_271.py`.
- `iterative_merge_sort.md`, the Part 1 explanation.
- The test file's output showing all checks passing (a pasted copy or a
  screenshot of the final run).
