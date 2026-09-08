"""
Array271 -- a fixed-capacity string array, built on top of a Python list.

Why this class exists
----------------------
Python's built-in `list` is a *dynamic* array: it grows and shrinks for you
automatically, and it can hold any mix of types. That convenience hides the
exact mechanics we're studying this week -- the ones a language like C or
Java exposes directly:

    - a fixed block of memory ("capacity") is reserved up front
    - the array tracks how much of that block is actually in use
      ("occupancy")
    - once the block is full, growing means allocating a *new*, larger
      block and copying everything over -- the old block cannot simply
      stretch in place, because the memory right after it may already
      belong to something else

Array271 pretends Python lists don't auto-resize. We use a plain list only
as the underlying storage (Python gives us no lower-level array type to
use directly), but we manage capacity and occupancy ourselves, by hand,
exactly like a fixed-capacity array would.

This file is intentionally incomplete. The constructor and the `add`
method are fully implemented and documented -- study them, they show you
the pattern. The `resize` method is a stub: it's your job to complete it.
"""


class Array271:
    """A fixed-capacity array of strings, backed by a Python list.

    Fields (deliberately not private -- no leading underscores -- while
    we're still getting comfortable with objects; we'll revisit
    encapsulation later in the course):

        capacity (int):
            How many string slots this array currently has room for,
            whether they're all in use or not.

        occupancy (int):
            How many of those slots are actually holding a string right
            now. Always satisfies 0 <= occupancy <= capacity.

        resize_factor (float):
            How aggressively the array grows when it runs out of room.
            Expressed as a fraction of the current capacity to add, e.g.
            0.25 means "grow capacity by 25% when you resize." You will
            use this number inside `resize`.

        items (list):
            The underlying Python list that actually stores the strings.
            It is pre-sized to `capacity` and padded with None in the
            slots that aren't occupied yet -- treat slots at index
            `occupancy` and beyond as empty, even though Python itself
            doesn't enforce that for us.
    """

    def __init__(self, capacity: int = 2, resize_factor: float = 0.25):
        """Construct an empty Array271.

        Parameters:
            capacity (int): initial number of slots to reserve. Defaults
                to 2, matching what we discussed in class -- small on
                purpose, so that a resize happens quickly in testing and
                isn't just a theoretical edge case.
            resize_factor (float): how much to grow capacity by (as a
                fraction of current capacity) when the array fills up.
                Defaults to 0.25 (grow by 25%), also from class.

        What this constructor sets up:
            - capacity and resize_factor are stored as given.
            - occupancy starts at 0: a brand-new array holds nothing.
            - items is created as a list of length `capacity`, with every
              slot initialized to None. None is a placeholder meaning
              "this slot exists in memory but has nothing useful in it
              yet" -- the same idea as uninitialized memory in a real
              fixed array, just made visible instead of hidden.
        """
        self.capacity: int = capacity
        self.resize_factor: float = resize_factor
        self.occupancy: int = 0

        # Pre-allocate the "block of memory": a list of exactly `capacity`
        # slots, all empty (None) for now. We never let this list grow or
        # shrink on its own -- only `resize` is allowed to replace it with
        # a new, differently-sized list.
        self.items: list = [None] * capacity

    def add(self, value: str):
        """Add a string to the array, growing it first if necessary.
        Parameters:
            value (str): the string to store next.

        Behavior:
            1. Check whether there's room: compare occupancy to capacity.
               If occupancy has reached capacity, there is no free slot
               left, so we must grow the underlying storage first by
               calling `resize()`.
            2. Once we're sure there's room (either there already was, or
               `resize()` just made some), place `value` into the array
               at index `occupancy` -- that's exactly the next free slot,
               since slots 0..occupancy-1 are already in use.
            3. Increment occupancy by 1, since we just filled one more
               slot.

        Note for students: `resize()` is currently just a stub (`pass`).
        Until you implement it, calling `add` on a full array will call
        `resize`, nothing will actually change, and the very next line
        (writing into `items[occupancy]`) will raise an IndexError,
        because the list still isn't big enough. That crash is a feature,
        not a bug -- it's your signal that `resize` needs real logic.
        """
        # Step 1: is the array full? occupancy == capacity means every
        # slot from 0 to capacity-1 is already holding a string.
        if self.occupancy == self.capacity:
            self.resize()

        # Step 2: place the new value in the next free slot.
        self.items[self.occupancy] = value

        # Step 3: record that one more slot is now in use.
        self.occupancy += 1

    def resize(self):
        new_capacity = int(self.capacity + (self.capacity * self.resize_factor)) # 1. the equation mentioned in the instructions.
                                                                                # make sure the result is an int
        if new_capacity <= self.capacity:                               # for instances such as 0.25 rounding to 0 seats. just add 1 if so.
            new_capacity += 1

        new_items = [None] * new_capacity                           # 2. a new list of the new capacity with every every slot set as None
        
        for i in range(self.occupancy):                            # 3. this copies every item from the old list to the new one by iterating it
            new_items[i] = self.items[i]

        self.items = new_items                                     # 4. replacing and updating self.items and self.capacity to the newer settings
        self.capacity = new_capacity
        """Grow the array's capacity when it's full. YOUR CODE GOES HERE.

        This method is intentionally left unimplemented (just `pass`).
        `add` already calls it at the right moment -- when occupancy has
        caught up to capacity -- so your job is only to make growing
        actually happen.

        Think through, and then implement, the following steps:

            1. Compute a new, larger capacity from the current one using
               `resize_factor`. For example, growing by resize_factor
               means: new_capacity = capacity + (capacity * resize_factor).
               Watch out for the case where that growth rounds down to
               zero extra slots (e.g. capacity=2, resize_factor=0.25 ->
               0.5 extra slots) -- a fixed array can't have a fractional
               number of slots, and growing by *zero* slots would defeat
               the whole purpose. Decide how you want to handle that, and
               be able to explain why.

            2. Allocate a new underlying list of that new capacity, with
               every slot initialized to None -- the same way `__init__`
               does it.

            3. Copy every currently-occupied string (indices 0 through
               occupancy - 1) from the old `items` list into the new one,
               in the same order and positions.

            4. Replace `self.items` with the new list, and update
               `self.capacity` to the new capacity. Do NOT touch
               `self.occupancy` here -- resizing changes how much room
               there is, not how many strings are actually stored.

        Questions to think about while you implement this (we'll discuss
        in class): Why copy element-by-element instead of just reusing
        the old list? What would go wrong if you updated `self.capacity`
        before finishing the copy? Is there any reason to ever *shrink*
        capacity, and would `resize_factor` still make sense for that?
        """
        pass
