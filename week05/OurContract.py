# ============================================================================
# NOTE ON TYPE HINTS
# ----------------------------------------------------------------------------
# The type hints in this file (e.g. "value: Any", "-> bool") are for
# DEMONSTRATION / ILLUSTRATIVE purposes only. Python does not enforce them
# at runtime -- they are documentation for readers and tools like mypy, not
# a guarantee. Passing an argument of the "wrong" type will not raise an
# error on its own.
# ============================================================================

from abc import ABC, abstractmethod
from typing import Any

class OurContract(ABC):
    """Interface every collection in this course must implement.

    Any class that inherits from OurContract (e.g. Array271, LinkedList271,
    ...) is required to provide a concrete body for each method below.
    Leaving one out -- or misspelling its name -- means Python will refuse
    to instantiate the subclass and raise a TypeError instead.
    """

    @abstractmethod
    def add(self, value: Any) -> None:
        """Insert value into the collection.

        Example: my_collection.add(42) should make 42 a member of the
        collection, growing the underlying storage first if there is no
        room left (see Array271.__resize for one way to do that).

        Parameters:
            value: the item to insert. No return value is expected.
        """
        pass

    @abstractmethod
    def contains(self, value: Any) -> bool:
        """Report whether value is already present in the collection.

        Example: my_collection.contains(42) should return True only if
        some element equal to 42 was previously added and not removed.

        Parameters:
            value: the item to look for.
        Returns:
            bool: True if value is found, False otherwise.
        """
        pass

    @abstractmethod
    def index_of(self, value: Any) -> list:
        """Find the position of value within the collection.

        Example: if the collection currently holds ["a", "b", "c"], then
        index_of("b") should return [1].

        Parameters:
            value: the item to search for.
        Returns:
            A list with the integer position of the item or
            an empty list if value is not present
        """
        pass

    @abstractmethod
    def indices(self, value: Any) -> list:
        """Find every position at which value occurs in the collection.

        Unlike index_of, which stops at the first match, indices reports
        all of them, in increasing order (front to back).

        Example: if the collection currently holds ["b", "a", "n", "a",
        "n", "a"], then indices("a") should return [1, 3, 5], indices("n")
        should return [2, 4], and indices("z") should return an empty
        list, []. A value that occurs exactly once yields a one-element
        list, e.g. indices("b") returns [0].

        Parameters:
            value: the item to search for.
        Returns:
            list: the integer positions of every element equal to value,
            in increasing order, or an empty list if value is not present.
            The collection itself is not modified.
        """
        pass

    @abstractmethod
    def count(self, value: Any) -> int:
        """Report how many times value occurs in the collection.

        Example: if the collection currently holds ["a", "b", "a"], then
        count("a") should return 2 and count("z") should return 0. This
        is analogous to Python's built-in list.count(value).

        Parameters:
            value: the item to count occurrences of.
        Returns:
            int: how many elements in the collection equal value.
        """
        pass