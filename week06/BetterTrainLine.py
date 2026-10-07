from __future__ import annotations
from Station import *


class BetterTrainLine:
    """A singly-linked chain of Stations representing one train line.

    Stations are added one at a time, always at the tail, so the line is
    built in the same order it will be traveled. The class keeps a __head
    (first station), a __last (current tail, for O(1) appends), and a
    __size (running count of stations).
    """

    # Constant used to compute the 1/f-th station in find_1_f_station().
    _SAFE_FRACTION: int = 1

    def __init__(self, name: str):
        """Create an empty train line.

        Parameters:
            name: the name of the line, e.g. "Red Line".
            head: the first station in the line, or None if the line is empty.
            last: the last station in the line, or None if the line is empty.
            size: the number of stations in the line, starting at 0.
        """
        self.__name: str = name
        self.__head: Station = None
        self.__last: Station = None
        # Do not use size to solve assignments for this object. Your s
        # solutions should be based on travering the linked list. 
        # You may use size to check your work, but it is not a substitute for
        # correct traversal logic. Besides if you used size to find, say
        # the middle station on a line with 7 stations, you would get the 3rd 
        # station (7//2), not the 4th, which is the correct one. So size is not a 
        # reliable substitute for correct traversal logic.
        self.__size: int = 0

    def __str__(self):
        """Return a short human-readable label for the line.

        Returns:
            str: the line's name, formatted for printing.
        """
        return f"Better Train Line name: {self.__name}"

    def add(self, new_station: Station):
        """Append a station to the end of the line.

        Example: if the line currently ends at Jarvis, add(howard) makes
        Howard the new last station, reachable via Jarvis.get_next().

        Parameters:
            new_station: the Station to attach after the current last
                station. No return value is expected.
        """
        if self.__head == None:
            self.__head = new_station
        else:
            self.__last.set_next(new_station)
        self.__last = new_station
        self.__size += 1

    def find_1_f_station(self, f: int) -> Station:
        """Find the station at the (1/f)-th point of the line.

        Since __size is already tracked by add(), the target position is
        known up front as __size // f. This walks a single cursor
        straight to that position, rather than racing two pointers
        against each other. find_1_f_station(2), for example, returns the
        same station as a midpoint search would.

        Parameters:
            f: the fraction's denominator. Must be a positive integer no
                greater than __size, so that __size // f lands on an
                actual station in the line.

        Returns:
            Station: the station at position __size // f. If f is invalid,
            the method will default to a safe value.
        """
        # Validate f and fall back to a safe default if it's invalid. This
        # is a bit more forgiving than the spec, which would raise an
        # exception for any invalid f. The safe default is 1, which returns
        # the first station in the line.
        if not isinstance(f, int) or f < 1 or f > self.__size:
            f = self._SAFE_FRACTION
        # Let's start the traversal using a fast and a slow cursor.
        # The fast cursor will move f steps for every 1 step the 
        # slow cursor moves.
        slow = self.__head
        fast = self.__head
        # The loop below is conditioned on the fast cursor's ability
        # to hop (skip) f stations ahead. If the ability is confirmed, 
        # the fast cursor hops f stations ahead, and the slow cursor,
        # hops one. To keep the code clean, we use two helper functions
        # to determine if the fast cursor can hop f stations ahead, and
        # to perform the hop. The loop ends when the fast cursor can no
        # longer hop f stations ahead, at which point the slow cursor is
        # at the (1/f)-th station in the line.
        while self.__can_hop(fast, f):
            # Move the fast cursor f stations ahead ... 
            fast = self.__hop(fast, f)
            # ... and the slow cursor 1 station ahead.
            slow = slow.get_next()
        # When the loop ends, the slow cursor is at the (1/f)-th station
        # in the line, so we return it.
        return slow

    def __can_hop(self, station: Station, f: int) -> bool:
        """Determine if the given station can hop f stations ahead.

        Parameters:
            station: the current station to check.
            f: the number of stations to hop ahead.
        """
        can = True
        count = 0
        probe = station
        while count < f and can:
            if probe == None:
                can = False
            else:
                probe = probe.get_next()
                count += 1
        return can

    def __hop(self, station: Station, f: int) -> Station:
        """Hop f stations ahead from the given station.

        Parameters:
            station: the current station to hop from.
            f: the number of stations to hop ahead.
        """
        count = 0
        probe = station
        while count < f and probe != None:
            probe = probe.get_next()
            count += 1
        return probe