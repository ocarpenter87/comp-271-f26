"""
TrainLine271: the BetterTrainLine we wrote in class on 9/25, promoted to
a full member of the 271 family by honoring the OurContract interface.

A train line is a chain of Station objects. The line itself remembers
only two of them: the head (the first station) and the last station.
Every other station is reached by starting at the head and following
get_next() one station at a time -- no skipping ahead.

Whoever uses a TrainLine271 works with station NAMES (strings), never
with Station objects. add("Howard") builds the Station itself; searches
take a name and report positions. The Station class is an internal
detail of the line, the same way the underlying list is an internal
detail of Array271.

Positions are counted from the head, starting at 0: on the line
Howard -> Jarvis -> Morse, Howard is at 0 and Morse is at 2.

Your job: replace every "TODO" below. Do not change the signatures.
Follow the course rules: one return statement per method, no break, no
imports beyond abc, typing, __future__, OurContract, and Station, no
magic numbers.
"""

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
        new_station = Station(value)
        if self.__head == None:
            self.__head = new_station
        else:
            self.__last.set_next(new_station)
        self.__last = new_station

    def contains(self, value: str) -> bool:
        return len(self.index_of(value)) > 0

    def index_of(self, value: str) -> list:
        current_station = self.__head
        result = []
        i = 0
        while current_station is not None and len(result)==0:
            if current_station.get_name() == value:
                result = [i]
            current_station = current_station.get_next()
            i += 1
        return result

    def indices(self, value: str) -> list:
        current_station = self.__head
        result = []
        i = 0
        while current_station is not None:
            if current_station.get_name() == value:
                result += [i]
            current_station = current_station.get_next()
            i += 1
        return result

    def count(self, value: str) -> int:
        return len(self.idices(value))
