# Solution: `find_e_f_station`

Worked solution for `better_train_line_271.py`'s one TODO this week.
`add_list` and `get_names` are already filled in and unchanged from the
version you were given — the only thing to write is `find_e_f_station`.

```python
def find_e_f_station(self, e: int, f: int) -> Station:
    """Find the station e out of every f stations down the line.

    Generalizes find_1_f_station (the e=1 case) one step further:
    slow now advances e stations per iteration while fast still
    advances f, so find_e_f_station(1, f) must land on the same
    station as find_1_f_station(f). Do this with a traversal only --
    no self.__size, no // anywhere in this method.

    Parameters:
        e: numerator of the fraction of the line to walk to.
        f: denominator of the fraction of the line to walk to. You
            may assume e and f are positive integers with e < f;
            you do not need to validate them for this assignment.
    Returns:
        Station: the e/f station.
    """
    slow: Station = self.__head
    fast: Station = self.__head
    while self.__can_hop(fast, f):
        for _ in range(e):
            slow = slow.get_next()
        for _ in range(f):
            fast = fast.get_next()
    return slow
```

## Why this is really `find_1_f_station` with one number unlocked

`find_1_f_station` already has the right shape: `fast` sweeps ahead `f`
stations at a time, `slow` trails behind, and the loop stops the moment
`fast` can't complete one more full `f`-station hop — at that point
`slow` has ended up `1/f` of the way down the line. The only thing
hard-coded in that version is how far `slow` moves each round: exactly
one station, every time, because `find_1_f_station` only ever needed the
numerator `1`.

`find_e_f_station` unlocks that number. `slow` now advances `e` stations
per iteration instead of `1`, using the exact same `for _ in range(e):
slow = slow.get_next()` shape that `fast` already uses for `f`. The stop
condition doesn't change at all — it's still `self.__can_hop(fast, f)`,
checking *`fast`'s* reach, because `fast` is still the one sweeping the
denominator. That's also *why* `find_e_f_station(1, f)` has to land on
the same station as `find_1_f_station(f)`: set `e = 1` here and the two
methods are doing character-for-character the same work, one station at
a time versus `e` stations at a time just happening to be the same thing
when `e` is `1`.

## Tracing `find_e_f_station(2, 3)` on `A-B-C-D-E-F-G`

Two rounds, both `slow` and `fast` starting at `A`:

| Round | `can_hop(fast, 3)`? | `slow` moves 2 | `fast` moves 3 |
|---|---|---|---|
| 1 | `A` can reach `D` — yes | `A → C` | `A → D` |
| 2 | `D` can reach `G` — yes | `C → E` | `D → G` |
| 3 | `G` has no next — no | *(loop stops)* | |

`slow` ends on `E` — two-thirds of the way down a seven-station line,
matching the hand-trace the assignment asks for.

## Turning it in

This is a worked model to check your own `find_e_f_station` against, not
a substitute for running the tests yourself —
`python3 test_better_train_line_271.py` against this file prints
`All tests passed.` for all 14 tests, including the two that confirm
`find_e_f_station(1, f)` reduces to `find_1_f_station(f)` exactly and
that neither `self.__size` nor `//` appears anywhere in the method's own
source.
