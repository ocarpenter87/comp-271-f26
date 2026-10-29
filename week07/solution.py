"""Reference solution for the Week 7 Mystery Sorters assignment.

Times gandalf, saruman, and sauron ONE AT A TIME, growing n by a fixed
step (never doubling), and drops a function as soon as either stopping
rule fires:

  rule 1 -- a single call takes longer than PER_CALL_CUTOFF_SECONDS, or
  rule 2 -- the total time spent on that function passes
            PER_FUNCTION_BUDGET_SECONDS.

The one thing that differs between the functions is WHERE they start.
gandalf and saruman start at n = 16, as the assignment says. sauron is
timed from n = 2 instead: at n = 16 a single call can take longer than
anyone is willing to wait, so there would be nothing to measure. Starting
tiny lets us watch its time explode as n creeps up by 1, which is the
evidence we need. See testing_guide.md for the reasoning.

Run it with:    python3 solution.py
"""

import random
import signal
import time

from comp271_mystery_sorters import gandalf, saruman, sauron

# How many fresh random lists we time at each size, then average.
TRIALS_PER_SIZE = 3
# The range of the random integers in each list.
MAX_VALUE = 1_000_000
# Rule 1: one call slower than this is "uncomfortably long".
PER_CALL_CUTOFF_SECONDS = 8
# Rule 2: total wall-clock time we allow ourselves on one function.
PER_FUNCTION_BUDGET_SECONDS = 60.0

# Each function's own starting size and step. These are the only numbers
# that differ between the three experiments.
GANDALF_START, GANDALF_STEP = 16, 2
SARUMAN_START, SARUMAN_STEP = 16, 2
SAURON_START, SAURON_STEP = 2, 1


class _TimedOut(Exception):
    """Raised by the alarm when one call runs past the per-call cutoff."""


def _raise_timed_out(signum, frame):
    """Alarm handler: turn the operating system's alarm into an exception
    that the try/except below can catch."""
    raise _TimedOut()


def timed_call(fn, n: int) -> float | None:
    """Time one call to fn on a fresh random list of size n.

    The alarm interrupts a call that outlives the cutoff, so a function
    that would run for hours (sauron, at n = 16) cannot hang this script.

    Returns:
        elapsed seconds, or None if the call was interrupted.
    """
    # A fresh list each time, built BEFORE the clock starts, so list
    # creation isn't counted as sorting time.
    data = [random.randint(0, MAX_VALUE) for _ in range(n)]
    signal.signal(signal.SIGALRM, _raise_timed_out)
    signal.alarm(PER_CALL_CUTOFF_SECONDS)
    elapsed = None
    try:
        start = time.perf_counter()
        fn(data)
        elapsed = time.perf_counter() - start
    except _TimedOut:
        elapsed = None
    finally:
        # Cancel the alarm whether the call finished or was interrupted.
        signal.alarm(0)
    return elapsed


def time_one(fn, n: int) -> float | None:
    """Average TRIALS_PER_SIZE fresh-list calls at size n.

    Returns:
        the average in seconds, or None if any trial was interrupted.
    """
    total = 0.0
    trial = 0
    # Pessimistic default: assume the size is too slow until every trial
    # has finished.
    average = None
    finished = True
    while trial < TRIALS_PER_SIZE and finished:
        elapsed = timed_call(fn, n)
        if elapsed is None:
            finished = False
        else:
            total += elapsed
            trial += 1
    if finished:
        average = total / TRIALS_PER_SIZE
    return average


def explore(fn, name: str, start: int, step: int) -> list[tuple[int, float]]:
    """Step n from `start` by `step`, recording (n, average time), until
    either stopping rule fires.

    Returns:
        every (n, average time) point recorded, in order.
    """
    n = start
    results: list[tuple[int, float]] = []
    budget_start = time.perf_counter()
    keep_going = True
    while keep_going:
        average = time_one(fn, n)
        if average is None:
            print(f"{name}: n={n:>6}  a call passed "
                  f"{PER_CALL_CUTOFF_SECONDS}s -- dropping")
            keep_going = False
        else:
            results.append((n, average))
            if time.perf_counter() - budget_start > PER_FUNCTION_BUDGET_SECONDS:
                print(f"{name}: stopped at n={n} (avg {average:.6f}s) -- "
                      f"{PER_FUNCTION_BUDGET_SECONDS}s budget used, "
                      f"{len(results)} points")
                keep_going = False
            else:
                n += step
    return results


def report(name: str, points: list[tuple[int, float]]):
    """Print the first, last, and an evenly sampled handful of points."""
    SAMPLES = 8
    print(f"\n{name}: {len(points)} points")
    if points:
        stride = max(1, len(points) // SAMPLES)
        shown = points[::stride]
        if shown[-1] != points[-1]:
            shown.append(points[-1])
        for n, average in shown:
            print(f"  n={n:>6}  {average:.6f}s")


if __name__ == "__main__":
    report("gandalf", explore(gandalf, "gandalf", GANDALF_START, GANDALF_STEP))
    report("saruman", explore(saruman, "saruman", SARUMAN_START, SARUMAN_STEP))
    report("sauron", explore(sauron, "sauron", SAURON_START, SAURON_STEP))
