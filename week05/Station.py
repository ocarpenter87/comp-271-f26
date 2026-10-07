from __future__ import annotations

class Station:

    def __init__(self, name:str):
        self.__name: str = name
        self.__next: Station = None

    def __str__(self):
        next_station: str = '(None)'
        if self.__next is not None:
            next_station = self.__next.get_name()
        return f"[{self.__name}] --> [{next_station}]"

    def get_name(self) -> str:
        return self.__name

    def get_next(self) -> Station:
        return self.__next

    def has_next(self) -> bool:
        return self.__next is not None

    def set_next(self, next:Station):
        self.__next = next


if __name__ == "__main__":
    how = Station('Howard')
    jar = Station('Jarvis')

    print("\nBefore:")
    print(how)
    print(jar)

    how.set_next(jar)

    print("\nAfter:")
    print(how)
    print(jar)
