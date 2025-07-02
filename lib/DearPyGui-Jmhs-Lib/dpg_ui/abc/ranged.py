from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import final


@dataclass(kw_only=True)
class Ranged[T](ABC):
    """Имеет Диапазон"""

    type Range = tuple[T, T]
    """Диапазон значений"""

    _range_max: T
    """Максимальное допустимое значение"""

    _range_min: T
    """Минимальное допустимое значение"""

    @abstractmethod
    def _onRangeMinChanged(self, new_min: T) -> None:
        """При изменении минимального значения"""

    @abstractmethod
    def _onRangeMaxChanged(self, new_max: T) -> None:
        """При изменении максимального значения"""

    @final
    def getRangeMax(self) -> T:
        """Получить максимальное допустимое значение"""
        return self._range_max

    @final
    def getRangeMin(self) -> T:
        """Получить минимальное допустимое значение"""
        return self._range_min

    @final
    def getRange(self) -> Range:
        """Получить диапазона"""
        return (
            self.getRangeMin(),
            self.getRangeMax()
        )

    @final
    def setRange(self, new_range: Range) -> None:
        """Установить диапазон"""
        new_min, new_max = new_range
        self.setRangeMin(new_min)
        self.setRangeMax(new_max)

    @final
    def setRangeMax(self, new_min: T) -> None:
        """Установить минимальное допустимое значение"""
        self._range_min = new_min
        self._onRangeMinChanged(new_min)

    @final
    def setRangeMin(self, new_max: T) -> None:
        """Установить минимальное допустимое значение"""
        self._range_max = new_max
        self._onRangeMinChanged(new_max)
