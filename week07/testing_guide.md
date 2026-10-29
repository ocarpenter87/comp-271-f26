# How the Testing Was Meant to Be Done

This explains the method behind the Week 7 assignment: what you measure, in
what order, and why. The [solution](solution.md) shows the numbers it
produces, and [`solution.py`](solution.py) is a working harness.

## The idea in one sentence

Time each function on bigger and bigger lists, and let how the time grows
tell you what the function is doing, without looking inside it.

## 1. One measurement is not a measurement

The computer is doing other things while your function runs. For each size
$n$:

1. Build a **fresh random list** of $n$ integers.
2. Start `time.perf_counter()`, call the function once, stop the clock.
   The list is built *before* the clock starts, so you time the sort, not
   the list building.
3. Repeat 3 to 5 times, each with a new random list, and **average**.

That average is one data point: `(n, average time)`.

## 2. One function at a time

Don't run all three functions through one shared list of sizes. Finish a
function completely, then move on. Each function decides for itself how far
you can push it, and the **size where you had to stop** is itself evidence.

## 3. Two stopping rules, and why both

Drop a function when **either** happens:

- **Rule 1, one call is too slow.** A single call passes your limit (5 to 10
  seconds is reasonable).
- **Rule 2, the whole experiment is too slow.** The total time you have
  spent on that function passes a budget (60 to 90 seconds).

With small steps, a slow function never has one dramatic call. It just gets
slightly slower each step, and the total quietly grows. Rule 2 catches that.
For `gandalf` and `saruman` it is Rule 2 that stops you. Rule 1 exists for
the function that is already too slow at the very start.

## 4. How to enforce Rule 1

Checking the time *after* a call returns can't stop a call that never
returns. Three ways around it, from simplest to most robust:

- **Ctrl-C.** If a run seems stuck, press it once, and write down the size
  you were on. Fine for a first try, but a script that handles it
  (`except KeyboardInterrupt`) keeps going to the next function.
- **`signal.alarm`.** Ask the operating system to interrupt the call after N
  seconds. This is what `solution.py` does (macOS and Linux only).
- **A separate process** that you can stop. The most portable approach.

## 5. Sauron: start small

This is the part that took some students a long time.

`sauron` is a *very* slow function. At $n = 16$ a single call can run for
years, so a harness that starts at 16 for every function sits waiting and
learns nothing. The instructions say to start at 16, and for `gandalf` and
`saruman` that is right. **For `sauron`, start at $n = 2$ and add 1.**

Here is what a run looks like (these are real numbers):

| $n$ | 5 | 6 | 7 | 8 | 9 | 10 |
|---|---|---|---|---|---|---|
| average time | 0.0003 s | 0.0008 s | 0.018 s | 0.069 s | 1.04 s | over 8 s |

Each step up by 1 multiplies the time, and the multiplier keeps growing.
That is a much stronger statement than "it timed out at 16", and it is the
evidence that separates "worse than polynomial" from "just slow".

Practical advice:

- **Expect to stop around $n = 9$ to 11.** That is the signal that it is
  working, not that something broke. Don't try to push past 11: each step
  up multiplies the time by about $n$, so $n = 10$ takes about 10 seconds,
  $n = 11$ about two minutes, $n = 12$ about twenty, and $n = 16$ years.
- **Stay with 5 or so trials per size.** Sauron is random: one call can get
  lucky and finish quickly while the next takes ten times longer. Averaging
  matters more here than anywhere else.
- **The first few sizes are noise.** At $n = 2$ or 3 a call takes a few
  millionths of a second, which is at the limit of the clock. Look at
  $n = 5$ and up.
- **Compare steps, not just the end points.** Look at
  $t(n+1)/t(n)$, or two or three steps apart if the step-to-step values bounce.

## 6. How to read the data

**Estimating $k$.** If time grows like $n^k$, then
$k \approx \log(t_2/t_1) / \log(n_2/n_1)$ for two points far apart. A $k$
near 1 suggests linear or $n \log n$, near 2 quadratic. This applies to
`gandalf` and `saruman`. Use your first and last points, or the average of
the first few and the last few, which is less affected by noise.

**Telling linear from $n \log n$.** A $k$ of 1.1 doesn't separate them.
Compare two sizes where $n$ quadruples: linear predicts about 4x the time,
$n \log n$ predicts about 4.7x.

**Why Sauron has no $k$.** For a polynomial, $k$ stays about the same
wherever you measure it. For Sauron it keeps climbing as $n$ grows. That is
what "worse than any polynomial" means, and it is the reason to look at the
step-to-step multiplier instead.

**Your plot.** Plot every measured point. A smooth curve drawn through three
points shows you the curve-fitting tool, not the function. Sauron can go on
the same chart if you use $n \le 10$, but its line will shoot straight up
next to the others, and you may prefer a second chart for it.

## 7. What to report

- How many trials you averaged per point.
- Your step size for each function, and your Rule 1 and Rule 2 limits.
- The size where each function stopped, and which rule stopped it.
- Your plot, or a table sampled every 25th or 50th point plus the first
  and last.
- A conclusion for each function that cites **your** numbers or **your**
  plot.

Different computers give different times. Two students with different
budgets who both find "$k$ is near 2 for `saruman`" have both done it right.
