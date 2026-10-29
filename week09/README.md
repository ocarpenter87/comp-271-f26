# Week 9 Assignment — A Minimum Heap

## The task

A **priority queue** always gives back its *smallest* value first, no matter
the order in which values were added. A **minimum heap**, stored in a list,
is the standard way to build one.

- **Part A.** Complete the two methods that do the real work of a heap:
  `_bubble_up` and `_sink_down`.
- **Part B.** A design problem: an emergency department's waiting list,
  where patients are seen by severity and, within a severity, in a fair
  order. You describe a `Patient` class; you do not write code.

## What you're given

- [`heaps.ipynb`](./heaps.ipynb) — the class notes: how `add` and `get`
  restore the heap property, and how a complete binary tree maps onto a
  list. Read it first if you missed Friday.
- [`heap_assignment_271.ipynb`](./heap_assignment_271.ipynb) — the handout:
  explanation, scaffold and tests. You do not turn it in.
  - `MinHeap271` is complete except for `_bubble_up` and `_sink_down`.
  - The test cell prints `ok` or `FAIL` with a reason. Some tests fail on
    the untouched scaffold; that is expected. One test checks the heap
    property on the list itself after every operation.

As always, every function that returns a value has **exactly one `return`**.

---

## Part A — `MinHeap271`

`self.storage` holds the tree level by level, root at index 0. For a node
at index `p`: left child `2p + 1`, right child `2p + 2`, parent
`(p - 1) // 2`.

- **`_bubble_up()`** — runs after `add` appends a value. While the value is
  not at the root and is smaller than its parent, swap them and follow it up.
- **`_sink_down()`** — runs after `get` moves the last value to the root.
  While the value is not at a leaf, find its **smaller** child; if the value
  is greater, swap and follow it down, otherwise stop.

Before coding, trace both on paper: values `2, 8, 4`, then `add(1)`, then
two calls to `get`.

**Rules:** no `heapq`, and no `sorted()`, `.sort()`, `min()` or `max()` over
`storage`. Compare values only with `<` and `>`, so the heap works with
anything Python can compare, including tuples like `(2, "Ana")`.

## Part B — Who is seen next?

Patients have a severity: `1` life-threatening, `2` severe, `3` not
life-threatening. The rule:

1. A smaller severity is always called in first.
2. Among equal severities, the patient who **arrived first** goes first.

You may not modify `MinHeap271`; it only compares with `<` and `>`. Describe
a `Patient` class (fields, methods, and what each is for) that lets the heap
enforce both rules. `Patient(severity)` creates a patient, and arrival
numbers run `0, 1, 2, …` over all severities. The rest of the design is yours.

---

## What to submit

One file, `heap271.py`, containing:

- `MinHeap271` with `_bubble_up` and `_sink_down` completed (other methods
  unchanged);
- your answers, including the `Patient` description, as comments at the top;
- nothing that runs automatically.

It must pass the Part A tests in the notebook.
