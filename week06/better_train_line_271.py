from __future__ import annotations
from Station import *


class BetterTrainLine:
    """A singly-linked chain of Stations representing one train line.

    Stations are added one at a time, always at the tail, so the line is
    built in the same order it will be traveled. The class keeps a __head
    (first station), a __last (current tail, for O(1) appends), and a
    __size (running count of stations).
    """

    def __init__(self, name: str):
        """Create an empty train line.

        Parameters:
            name: the name of the line, e.g. "Red Line".
        """
        self.__name: str = name
        self.__head: Station = None
        self.__last: Station = None
        self.__size: int = 0

    def __str__(self):
        """Return a short human-readable label for the line.

        Returns:
            str: the line's name, formatted for printing.
        """
        return f"Better Train Line name: {self.__name}"

    def add(self, new_station: Station):
        """Append a station to the end of the line.

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

    def add_list(self, names: list):
        """Append a station for each name in names, in order.

        Example: add_list(["Howard", "Jarvis", "Morse"]) has the same
        effect as three separate calls, add("Howard"), add("Jarvis"),
        then add("Morse") — Howard becomes (or extends) the head, Morse
        ends up last.

        Parameters:
            names: a list of station names to add, front to back. No
                return value is expected.
        """
        for name in names:
            self.add(Station(name))

    def get_names(self) -> list:
        """Return the names of every station, in order of traversal.

        Example: on Howard -> Jarvis -> Morse, get_names() returns
        ["Howard", "Jarvis", "Morse"]. On an empty line, it returns [].

        Returns:
            list: the station names front to back. The line itself is
            not modified.
        """
        names: list = []
        current: Station = self.__head
        while current is not None:
            names.append(current.get_name())
            current = current.get_next()
        return names

    def find_middle_station(self) -> Station:
        """Find the station halfway down the line in one pass.

        Classic fast/slow sweep: slow advances one station per iteration
        while fast advances two, so fast reaches the end (or falls one
        station short of it) right as slow reaches the midpoint.

        Returns:
            Station: the middle station.
        """
        slow: Station = self.__head
        fast: Station = self.__head
        while fast.has_next() and fast.get_next().has_next():
            slow = slow.get_next()
            fast = fast.get_next().get_next()
        return slow

    def find_one_third_station(self) -> Station:
        """Find the station one third of the way down the line.

        Same fast/slow sweep as find_middle_station, except fast now
        advances three stations per iteration while slow still advances
        one, landing slow near the one-third point instead of the
        midpoint.

        Returns:
            Station: the one-third station.
        """
        slow: Station = self.__head
        fast: Station = self.__head
        while (
            fast.has_next()
            and fast.get_next().has_next()
            and fast.get_next().get_next().has_next()
        ):
            slow = slow.get_next()
            fast = fast.get_next().get_next().get_next()
        return slow

    def find_1_f_station(self, f: int) -> Station:
        """Find the station 1/f of the way down the line, for any f.

        Generalizes find_middle_station (f=2) and find_one_third_station
        (f=3) into a single method: slow still advances one station per
        iteration; fast advances f stations per iteration. Do this with a
        traversal only — no self.__size, no // anywhere in this method.

        Parameters:
            f: denominator of the fraction of the line to walk to. You
                may assume f is a positive integer; you do not need to
                validate it for this assignment.
        Returns:
            Station: the 1/f station.
        """
        slow: Station = self.__head
        fast: Station = self.__head
        while self.__can_hop(fast, f):
            slow = slow.get_next()
            for _ in range(f):
                fast = fast.get_next()
        return slow

    def find_e_f_station(self, e: int, f: int) -> Station:
        """Find the station e out of every f stations down the line.

        Generalizes find_1_f_station (the e=1 case) one step further:
        slow now advances e stations per iteration while fast still
        advances f, so find_e_f_station(1, f) must land on the same
        station as find_1_f_station(f). Do this with a traversal only —
        no self.__size, no // anywhere in this method.

        Parameters:
            e: numerator of the fraction of the line to walk to.
            f: denominator of the fraction of the line to walk to. You
                may assume e and f are positive integers with e < f;
                you do not need to validate them for this assignment.
        Returns:
            Station: the e/f station.
        """
        # TODO: same shape as find_1_f_station, but slow now advances e
        # stations per iteration (instead of 1) while fast still
        # advances f. Stop under the same condition as find_1_f_station
        # — as soon as fast can't complete one more full f-station hop.
        pass

    def __can_hop(self, station: Station, hops: int) -> bool:
        """Check whether station can advance hops stations without
        running off the end of the line.

        Parameters:
            station: the station to hop from.
            hops: how many stations ahead to check for.
        Returns:
            bool: True if hops consecutive get_next() calls starting at
            station would all succeed, False otherwise.
        """
        current: Station = station
        can_hop: bool = True
        for _ in range(hops):
            can_hop = can_hop and current.has_next()
            if can_hop:
                current = current.get_next()
        return can_hop


if __name__ == "__main__":
    line = BetterTrainLine("Red Line")
    for stop in ["Howard", "Jarvis", "Morse", "Loyola", "Granville"]:
        line.add(Station(stop))

    print(f"Middle station: {line.find_middle_station().get_name()}")
    print(f"One-third station: {line.find_one_third_station().get_name()}")

    # These print the same names as the two lines above.
    print(f"1/2 station: {line.find_1_f_station(2).get_name()}")
    print(f"1/3 station: {line.find_1_f_station(3).get_name()}")

    # Builds a second line identical in structure to the one built by
    # the loop above.
    other_line = BetterTrainLine("Red Line (via add_list)")
    other_line.add_list(["Howard", "Jarvis", "Morse", "Loyola", "Granville"])
    print(f"Other line's middle station: {other_line.find_middle_station().get_name()}")

    # Prints ['Howard', 'Jarvis', 'Morse', 'Loyola', 'Granville'].
    print(f"Names in order: {line.get_names()}")

    # Once find_e_f_station is implemented, these should print Morse and
    # Jarvis again — e=1 is the same case as find_1_f_station.
    # print(f"e/f=1/2 station: {line.find_e_f_station(1, 2).get_name()}")
    # print(f"e/f=1/3 station: {line.find_e_f_station(1, 3).get_name()}")
