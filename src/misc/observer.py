from typing import Any
from typing import Callable


class Subject[T]:
    """Субъект"""

    def __init__(self) -> None:
        self.__observers = list[Callable[[T], Any]]()

    def notifyObservers(self, value: T) -> None:
        """Уведомить наблюдателей"""
        for observer in self.__observers:
            observer(value)

    def addObserver(self, observer: Callable[[T], Any]) -> None:
        """Добавить наблюдателя"""
        self.__observers.append(observer)
