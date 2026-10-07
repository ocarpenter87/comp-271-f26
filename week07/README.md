# Week 7 Assignment: The Mystery Sorters

## The task

This week's class covered four sorting algorithms and how to reason
about their cost. This assignment gives you three "mystery" sorting
functions — `gandalf`, `saruman`, and `sauron` — and asks you to figure
out, purely from *timing* them, what each one is actually doing
underneath.

All three share one contract:

```python
def mystery_sort(a: list[int]) -> list[int]:
    ...
```

Each takes a list of integers and returns a **new**, sorted list. None
of them modifies the list you pass in. That's all you're told.

**Do not read the package's source to answer this assignment.** Yes,
it's an installable package, so nothing physically stops you from
downloading and opening it — but doing that defeats the point of the
exercise, which is to reason from behavior the same way you'd have to
with any library you didn't write and can't inspect.

## Setup

```
pip install comp271-mystery-sorters
```

```python
from comp271_mystery_sorters import gandalf, saruman, sauron
```

## What to turn in

A short write-up (code + text, however you want to present it) covering:

1. **How you timed each function.** Use `time.perf_counter()`, not
   `time.time()`. For each timing, generate a **fresh random list**
   and time one call; repeat several times (5 is reasonable) with a
   new random list each time, and average the results. One run is a
   sample, not a measurement.

2. **Work through one function at a time — don't test all three
   against one shared list of sizes.** For each function, in turn:

   - Start at $n = 16$.
   - Time it (averaged as above).
   - Double $n$ and time it again.
   - Keep doubling until either you have enough doublings (4–5) to see
     a clear pattern, **or** a single run starts taking uncomfortably
     long. Pick your own cutoff (10–30 seconds is reasonable) and stop
     the moment you cross it — record "stopped at $n=\ldots$, this size
     took $\ldots$ seconds" as your last data point. That's a real
     result, not a failure.
   - Only then move to the next function, starting over at $n = 16$.

   Doing it this way — one function to its own limit before starting
   the next — means that whichever function is going to blow up stops
   *you* quickly, instead of getting buried inside one shared loop
   where you don't notice it's the problem until a run has already
   been hanging for several minutes at a size you picked for a
   different function.

3. **Your data.** A table of size vs. average time for each function
   (note how many trials you averaged, and where — if at all — you
   stopped early).

4. **Your conclusion, with reasoning.** For each function, name the
   growth class you believe it falls into — $\Theta(n)$,
   $\Theta(n \log n)$, $\Theta(n^2)$, or "worse than any polynomial
   we've discussed" — and, if you're willing to commit, which specific
   algorithm (or something not covered in class at all) you think it
   is. **Cite your own numbers.** "It felt slow" isn't an argument;
   "time roughly quadrupled across four consecutive doublings" is. A
   wrong guess at the specific algorithm with solid reasoning from the
   data earns more credit than a right guess with no numbers behind it.
