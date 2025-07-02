from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import final


@dataclass(kw_only=True)
class Intervaled[T](ABC):
    """Имеет интервал"""

    type Interval = tuple[T, T]
    """Диапазон значений"""

    _interval_max: T
    """Максимальное допустимое значение"""

    _interval_min: T
    """Минимальное допустимое значение"""

    @abstractmethod
    def _onIntervalMinChanged(self, new_min: T) -> None:
        """При изменении минимального значения"""

    @abstractmethod
    def _onIntervalMaxChanged(self, new_max: T) -> None:
        """При изменении максимального значения"""

    @final
    def getIntervalMax(self) -> T:
        """Получить максимальное допустимое значение"""
        return self._interval_max

    @final
    def getIntervalMin(self) -> T:
        """Получить минимальное допустимое значение"""
        return self._interval_min

    @final
    def getInterval(self) -> Interval:
        """Получить диапазона"""
        return (
            self.getIntervalMin(),
            self.getIntervalMax()
        )

    @final
    def setIntervalMax(self, new_min: T) -> None:
        """Установить минимальное допустимое значение"""
        self._interval_min = new_min
        self._onIntervalMinChanged(new_min)

    @final
    def setIntervalMin(self, new_max: T) -> None:
        """Установить минимальное допустимое значение"""
        self._interval_max = new_max
        self._onIntervalMinChanged(new_max)

    @final
    def setInterval(self, new_range: Interval) -> None:
        """Установить диапазон"""
        new_min, new_max = new_range
        self.setIntervalMin(new_min)
        self.setIntervalMax(new_max)
