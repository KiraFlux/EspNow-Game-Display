from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import Callable


class Observer[T](ABC):
    """Наблюдатель"""

    @abstractmethod
    def update(self, value: T) -> None:
        """Обновить состояние"""


@dataclass
class InlineObserver[T](Observer):
    callback: Callable[[T], None]

    def update(self, value: T) -> None:
        self.callback(value)


class Subject[T]:
    """Субъект"""

    def __init__(self) -> None:
        self.__observers = list[Observer]()

    def notifyObservers(self, value: T) -> None:
        """Уведомить наблюдателей"""
        for observer in self.__observers:
            observer.update(value)

    def addObserver(self, observer: Observer[T]) -> None:
        """Добавить наблюдателя"""
        self.__observers.append(observer)
