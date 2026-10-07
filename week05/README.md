# Week 5 Assignment: `TrainLine271` — A Train Line That Honors the Contract

## The task

On Friday we built `BetterTrainLine`: a chain of `Station` objects with a
`head` and a `last` pointer, so adding a station takes the same few steps
no matter how long the line is. It can grow, but it can't answer a single
question about itself. This week you'll make it a full member of the 271
family by implementing `OurContract`: `add`, `contains`, `index_of`,
`indices`, and `count`.

`Array271` keeps its items side by side in memory and can jump to any
position. `TwoDimensional` does the same thing with a grid. A train line
can't jump anywhere. Every question it answers has to start at the head
and ride forward one station at a time. The five methods are the same;
how they work underneath is completely different.

## The data structure

- A `TrainLine271` has a name and remembers exactly two stations: the
  **head** (the first station) and the **last** station. An empty line
  has both set to `None`.
- Each `Station` knows its own name and its next station. That's
  `Station.py` from class, unchanged.
- **Users of the line work with names, not stations.** `add("Howard")`
  takes a string, and your code builds the `Station`. `index_of("Morse")`
  takes a string and reports a position. Nobody outside the class ever
  sees a `Station`. That is the contract doing its job: someone using a
  `TrainLine271` shouldn't need to know it is made of stations, just as
  someone using `Array271` doesn't need to know about its list.
- **Positions** count from the head, starting at `0`. On
  `Howard → Jarvis → Morse`, Howard is at `0` and Morse is at `2`.
- **Names can repeat.** The contract doesn't promise that values are
  unique, so your line must handle a name that appears more than once.

## What you're given

- `train_line_271.py` is the scaffold. The class header, constructor,
  `__str__`, and `get_name` are complete. Every contract method is a
  `TODO`.
- `Station.py` is the station class from class.
- `OurContract.py` is the contract, the same file as Week 4.
- `test_train_line_271.py` runs with:

  ```
  python3 test_train_line_271.py
  ```

  Two of the 13 tests pass against the scaffold as-is. When your
  implementation is correct, all 13 pass and the last line prints
  `All tests passed.`

## What you need to do

Complete these in `train_line_271.py`:

1. **`add(value)`**: wrap `value` in a new `Station` and attach it after
   the last station, the `BetterTrainLine` way. An empty line is the
   special case: the new station becomes both head and last. **Do not
   walk the line to find the end.** One test builds a 20,000-station
   line and fails if `add` takes time proportional to the line's length.
2. **`index_of(value)`**: a one-element list holding the position of the
   **first** station named `value`, e.g. `[2]`, or an empty list `[]` if
   there is none. Stop riding as soon as you find it.
3. **`indices(value)`**: a list holding the position of **every** station
   named `value`, front to back, e.g. `[1, 4]`, or `[]` if there is none.
   A single match is still a list: `[0]`.
4. **`contains(value)`**: delegate to `index_of`, as we did in class.
5. **`count(value)`**: how many stations are named `value`.

As announced in class on 9/23, `index_of` and `indices` return a list,
not a tuple. This updates `OurContract` for every implementation going
forward.

All of the searching methods walk the line the same way: start at the
head, look at the current station, move to its next, and stop when there
is no station left. Get that loop right once and the rest follows.

**Imports:** it is OK to import anything from the following modules, and
nothing else:

- [`abc`](https://docs.python.org/3/library/abc.html)
- [`typing`](https://docs.python.org/3/library/typing.html)
- [`__future__`](https://docs.python.org/3/library/__future__.html)
- `OurContract`, the contract we wrote for 271
- `Station`, the station class from class

**Rules, same as class:** one `return` per method (build up a result
variable); no `break`; no other imports; no magic numbers. Talk to a
`Station` only through its methods (`get_name`, `get_next`, `has_next`,
`set_next`), never its private fields. Do not change `Station.py` or any
method signature.

## Questions to be ready to discuss in class

- `add` takes a string, not a `Station`. What would a user of the line
  have to know if it took a `Station` instead? What could they break?
- Why does `add` need no traversal, while `index_of` does? Could a
  `last`-style pointer make `index_of` constant time too?
- In `Array271`, `index_of` walks the positions `0, 1, 2, …` and reads each
  item. What does your loop walk, and where does the position number come
  from?
- `index_of` stops at the first match, and `indices` never stops early.
  How does each loop's condition show that?
- With Friday's vocabulary, how does the time each of your five methods
  takes grow with the number of stations: constant or linear?
- `Array271`, `TwoDimensional`, and `TrainLine271` share no code. What
  can someone holding "some `OurContract`" count on, whichever one they
  were given?

## How to submit

Submit your completed `train_line_271.py` and confirm
`python3 test_train_line_271.py` prints `All tests passed.` at the end.
Due **Monday, October 5**, via Sakai.

## Reading

From the course's Runestone edition (*Problem Solving with Algorithms
and Data Structures using Python: The Interactive Edition*), Basic Data
Structures:

- [3. Lists](https://runestone.academy/ns/books/published/loyolauniversitychicago_pswadsup_fall26/basic-ds_lists.html)
- [The Unordered List Abstract Data Type](https://runestone.academy/ns/books/published/loyolauniversitychicago_pswadsup_fall26/basic-ds_the-unordered-list-abstract-data-type.html)
- [Implementing an Unordered List: Linked Lists](https://runestone.academy/ns/books/published/loyolauniversitychicago_pswadsup_fall26/basic-ds_implementing-an-unordered-list-linked-lists.html)
- [The Ordered List Abstract Data Type](https://runestone.academy/ns/books/published/loyolauniversitychicago_pswadsup_fall26/basic-ds_the-ordered-list-abstract-data-type.html)
