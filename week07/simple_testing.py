"""A simple timing harness for the Week 7 mystery sorters.

For each mystery function, this script starts with a tiny list (n = 2),
times the function on it, then doubles n and times it again, over and over.
For every n it prints one line: the size, and the average time one call took.
You then look at how those times grow as n grows.

Run it from a terminal with:

    python3 simple_testing.py

You are free to change this file: different sizes, different trial counts,
a different way of stepping n. The assignment asks you to explain HOW you
timed things, so make sure you understand every line before you hand in
results produced by it.
"""

import random
import time

# The package you installed with `pip install comp271-mystery-sorters`.
# Each name below is a function that takes a list of ints and returns a new,
# sorted list. We only ever call them; we never look inside them.
from comp271_mystery_sorters import gandalf, saruman, sauron

# How many times we time the function at each size. A single run is one
# sample, not a measurement: the computer is busy with other things, and
# different random lists can behave differently. Averaging several runs
# smooths that noise out.
TRIALS = 10

# How many seconds we allow ourselves to spend on ALL the trials at one
# value of n. Once a size costs more than this, we stop testing that
# function. Without a limit like this, a function that grows quickly would
# make us wait a very long time.
TIME_LIMIT = 0.5


def random_array(n: int) -> list[int]:
    """Build a list of n random integers between 0 and 10,000.

    A fresh list is built for every trial, so the average is not just a
    statement about one lucky (or unlucky) arrangement of numbers.
    """
    return [random.randint(0, 10_000) for _ in range(n)]


def average_time(func, n: int) -> tuple[float, float]:
    """Time func on TRIALS random lists of size n.

    Returns two numbers:
      * the average time of one call, in seconds (this is what we report), and
      * the total seconds spent on all the trials at this n (this is what we
        compare against TIME_LIMIT to decide when to stop).
    """
    total = 0.0
    for _ in range(TRIALS):
        data = random_array(n)

        # Use time.perf_counter(), not time.time(): it is designed for
        # measuring short intervals and has much finer resolution.
        # Only the call to func sits between the two readings, so building
        # the random list is NOT included in the measured time.
        start = time.perf_counter()
        func(data)
        total += time.perf_counter() - start

    return total / TRIALS, total


# Everything below runs only when you execute this file directly
# (python3 simple_testing.py), not when another file imports it.
if __name__ == "__main__":

    # Work through the functions one at a time. Each function starts over
    # at n = 2 and is dropped once it crosses the time limit, before we
    # move on to the next one.
    for function in [gandalf, saruman, sauron]:
        print(function.__name__)

        n = 2
        keep_going = True

        while keep_going:
            avg, spent = average_time(function, n)

            # One line per size: n, then the average seconds per call.
            # The :.6f formats the time with six digits after the decimal
            # point, so very small times still show up as nonzero.
            print(n, f"{avg:.6f}")

            # Double n for the next round: 2, 4, 8, 16, 32, ...
            # Doubling covers a huge range of sizes in only a few steps,
            # and comparing each time with the one before it (what happened
            # to the time when n doubled?) is a good way to spot the
            # growth pattern.
            n *= 2

            # Keep going only while this size stayed within the time limit.
            # We write this as a condition instead of using `break`, so the
            # loop has a single, obvious exit.
            keep_going = spent <= TIME_LIMIT

        # If the script ever seems stuck on one size for much longer than
        # you expected, you can stop it with Ctrl-C in the terminal. That is
        # useful information too: write down the size where it happened.
