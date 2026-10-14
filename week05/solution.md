# Solution: `TrainLine271`

Worked solution for `train_line_271.py`, completing the five `OurContract`
methods against the `BetterTrainLine` shape from class: a line that
remembers only its `head` and `last`, and answers every question by
walking from the head one station at a time.

```python
from __future__ import annotations

from OurContract import OurContract
from Station import Station


class TrainLine271(OurContract):

    def __init__(self, name: str):
        self.__name: str = name
        self.__head: Station = None
        self.__last: Station = None

    def __str__(self) -> str:
        return f"Train line name: {self.__name}"

    def get_name(self) -> str:
        return self.__name

    def add(self, value: str) -> None:
        new_station: Station = Station(value)
        if self.__head is None:
            self.__head = new_station
        else:
            self.__last.set_next(new_station)
        self.__last = new_station

    def contains(self, value: str) -> bool:
        result: bool = len(self.index_of(value)) > 0
        return result

    def index_of(self, value: str) -> list:
        result: list = []
        current: Station = self.__head
        position: int = 0
        found: bool = False
        while current is not None and not found:
            if current.get_name() == value:
                result = [position]
                found = True
            else:
                current = current.get_next()
                position += 1
        return result

    def indices(self, value: str) -> list:
        result: list = []
        current: Station = self.__head
        position: int = 0
        while current is not None:
            if current.get_name() == value:
                result.append(position)
            current = current.get_next()
            position += 1
        return result

    def count(self, value: str) -> int:
        result: int = len(self.indices(value))
        return result
```

## `add(value)` — constant time, no traversal

The whole point of keeping `__last` around is that attaching a station
never needs to know how long the line already is. An empty line is the
one special case: there's no `__last` to attach after, so the new
station becomes `__head` too. Either way, it ends as `__last`. This is
exactly `BetterTrainLine.add`'s shape from class, just building the
`Station` from the name passed in rather than receiving one ready-made —
`add` is the one place a caller's string becomes a `Station`; nothing
outside this method ever needs to.

## `index_of(value)` — stop as soon as you find it, without `break`

"Stop walking as soon as you find it" and "no `break`" sound like they're
in tension, but they're not: a loop can stop itself by putting the
stopping condition directly in its own `while` test. `found` starts
`False`; the loop's condition is `current is not None and not found`, so
the moment `found` flips to `True`, the *next* check of the condition
ends the loop on its own — no `break` needed, and still only one
`return`, at the very end, with `result` sitting at `[]` the whole time
until (and unless) a match sets it to `[position]`.

## `indices(value)` — the same walk, nothing stops it early

`indices` is `index_of` with the early-stop condition removed: walk
every station, and whenever the name matches, append the current
position to `result` instead of replacing it. The loop's own condition —
`current is not None` — is the only thing that ends it; nothing about
finding a match changes the loop's behavior, which is exactly what "no
early stop" looks like in code rather than in words.

## `contains(value)` and `count(value)` — delegate, don't re-walk

`contains` is the one case from class: a name is present exactly when
`index_of` finds at least one match, so `contains` never needs its own
traversal — `len(self.index_of(value)) > 0` says exactly that. `count`
follows the same idea one level up: the number of matches *is* the
length of `indices`' own result, so `count` delegates to `indices`
rather than walking the line a third time with its own copy of the same
loop. Four methods, two traversals.

## Turning it in

This is a worked model to check a submission against, not a substitute
for running your own tests — `python3 test_train_line_271.py` against
this file prints `All tests passed.` for all 13 tests, including the
one that builds a 20,000-station line to confirm `add` doesn't slow down
as the line grows; that's the test to run against your own `add` first
if anything here doesn't match.
