from abc import ABC
from abc import abstractmethod


class Observer[T](ABC):
    """Наблюдатель"""

    @abstractmethod
    def update(self, value: T) -> None:
        """Обновить состояние"""


class Subject[T](ABC):
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
