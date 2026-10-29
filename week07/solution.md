# Solution: The Mystery Sorters

A worked answer to the [Week 7 assignment](README.md), produced by running
[`solution.py`](solution.py) against the real `comp271_mystery_sorters`
package. How the experiment is meant to be run (and why Sauron is handled
differently) is in [`testing_guide.md`](testing_guide.md). Your own numbers
will differ from these: your computer, your increment, and your budget are
not mine. What should match is the **shape** of each curve and the rough
size of $k$.

Settings: 3 trials per size, an 8-second per-call cutoff (enforced with
`signal.alarm`), a 60-second budget per function. `gandalf` and `saruman`
start at $n = 16$ and step by 2. `sauron` starts at $n = 2$ and steps by 1.

## `gandalf`

3,067 points, $n = 16 \to 6{,}148$. Stopped on the **60-second budget**, not
the per-call cutoff: no single call took more than about 0.011 s.

| $n$ | average time (s) |
|---:|---:|
| 16 | 0.000017 |
| 782 | 0.001123 |
| 1,548 | 0.002407 |
| 2,314 | 0.003834 |
| 3,080 | 0.005186 |
| 3,846 | 0.006668 |
| 4,612 | 0.008444 |
| 5,378 | 0.009953 |
| 6,148 | 0.011112 |

First and last points: $k \approx \log(0.011112/0.000017) /
\log(6148/16) \approx 1.09$. Close to linear, with a curve that bends up
very slightly. That is what $\Theta(n \log n)$ looks like: a linear term
carrying a slowly growing $\log n$ factor.

**Conclusion: $\Theta(n \log n)$. It is merge sort.**

A $k$ near 1.09 can't by itself separate $n \log n$ from plain linear. A
second check can: compare two sizes where $n$ quadruples. Linear predicts
4x the time, $n \log n$ predicts about 4.7x. Here $n = 1{,}548 \to
6{,}148$ (about 4x) took $0.002407 \to 0.011112$ s, a factor of 4.6.

## `saruman`

696 points, $n = 16 \to 1{,}406$. Also stopped on the **60-second budget**
(last call 0.083 s, nowhere near the cutoff).

| $n$ | average time (s) |
|---:|---:|
| 16 | 0.000013 |
| 190 | 0.001268 |
| 364 | 0.004769 |
| 538 | 0.011551 |
| 712 | 0.020215 |
| 886 | 0.032077 |
| 1,060 | 0.047647 |
| 1,234 | 0.064662 |
| 1,406 | 0.083488 |

First and last points: $k \approx \log(0.083488/0.000013) /
\log(1406/16) \approx 1.96$. The curve bends sharply upward. Under the same
60 seconds it reached only about a quarter of `gandalf`'s $n$, which is
itself evidence that it grows faster.

**Conclusion: $\Theta(n^2)$. It is bubble sort** (with an early exit when a
pass makes no swaps). Insertion sort and selection sort would give nearly
the same curve on random input; timing alone cannot tell them apart.

## `sauron`

Sauron can't be run the way the other two are. At $n = 16$ a single call
runs far past any cutoff, so starting at 16 gives you a timeout and no data.
Starting small gives you data:

| $n$ | average time (s) |
|---:|---:|
| 2 | 0.000021 |
| 3 | 0.000006 |
| 4 | 0.000033 |
| 5 | 0.000299 |
| 6 | 0.000755 |
| 7 | 0.017505 |
| 8 | 0.068601 |
| 9 | 1.036722 |
| 10 | stopped: a call passed 8 s |

Three things in this table matter:

1. **Adding one to $n$ multiplies the time.** From 7 to 8 the time grew
   about 4x, and from 8 to 9 about 15x. Compare `saruman`, where adding 2
   to $n$ raises the time by well under 1%.
2. **The multiplier grows as $n$ grows.** For $n^2$ it would shrink toward
   1; here it climbs. Going from 7 to 9 (two steps) took the time up about
   59x. A factorial predicts $9!/7! = 72$.
3. **It is noisy.** The multiplier from step to step bounces (2.5x, then 23x,
   then 4x, then 15x) because Sauron sorts by shuffling at random, so one
   call can get lucky and the next take 10 times longer. That is why the
   average over several fresh lists matters more here than anywhere else,
   and why we compare steps that are two or three apart.

**Conclusion: worse than any polynomial, roughly factorial. It is bogosort**
(shuffle at random until the list happens to be sorted). A list of $n$
distinct numbers has $n!$ orderings and only one is sorted, so it needs about
$n!$ shuffles on average. At $n = 16$ that is about $2 \times 10^{13}$.

A $k$ estimate is not meaningful for Sauron: the exponent would keep
climbing as $n$ grows, which is what "worse than polynomial" means.

## What full credit looked like

- The method: fresh random lists, `time.perf_counter()`, an average per size,
  one function at a time, both stopping rules stated.
- Your own numbers or your own plot cited in the argument.
- $k \approx 1$ to 1.2 for `gandalf` and $k \approx 1.9$ to 2.1 for
  `saruman`, or a description of the same shapes.
- For `sauron`: a statement that its time multiplies as $n$ grows by one,
  with the sizes you measured, or at least that a call at $n = 16$ never
  finished. Naming bogosort was optional.
- A note that the three functions stopped at very different $n$ under the
  same budget, and what that says.
