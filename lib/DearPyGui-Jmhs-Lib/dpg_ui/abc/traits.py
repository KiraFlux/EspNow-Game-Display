from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import final

from lina.vector import Vector2D
from rs.color import Color


@dataclass(kw_only=True)
class Colored(ABC):
    """Содержит цвет"""

    _color: Color
    """Цвет"""

    @abstractmethod
    def setColor(self, color: Color) -> None:
        """Изменить цвет"""

    @final
    def getColor(self) -> Color:
        """Получить актуальный цвет"""
        return self._color


@dataclass(kw_only=True)
class Intervaled[T](ABC):
    """Имеет интервал"""

    type Interval = tuple[T, T]
    """Диапазон значений"""

    _interval_max: T
    """Максимальное допустимое значение"""

    _interval_min: T
    """Минимальное допустимое значение"""

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

    @abstractmethod
    def setIntervalMax(self, new_max: T) -> None:
        """Установить минимальное допустимое значение"""

    @abstractmethod
    def setIntervalMin(self, new_min: T) -> None:
        """Установить минимальное допустимое значение"""

    @final
    def setInterval(self, new_range: Interval) -> None:
        """Установить диапазон"""
        new_min, new_max = new_range
        self.setIntervalMin(new_min)
        self.setIntervalMax(new_max)


@dataclass(kw_only=True)
class Valued[T](ABC):
    """Содержит значение"""

    _value: T
    """Значение по умолчанию"""

    @abstractmethod
    def setValue(self, value: T) -> None:
        """Установить значение"""

    @abstractmethod
    def getValue(self) -> T:
        """Получить актуальное значение"""


@dataclass(kw_only=True)
class Sizable[T: (int, float)](ABC):
    """Объект с управляемыми размерами"""

    _width: T = 0
    """Изначальная ширина"""

    _height: T = 0
    """Изначальная высота"""

    @abstractmethod
    def getWidth(self) -> T:
        """Получить актуальную ширину"""

    @abstractmethod
    def getHeight(self) -> T:
        """Получить актуальную высоту"""

    @final
    def getSize(self) -> Vector2D[T]:
        """Получить актуальный размер"""
        return Vector2D(
            self.getWidth(),
            self.getHeight()
        )

    def setWidth(self, new_width: T) -> None:
        """Установить ширину"""

    def setHeight(self, new_height: T) -> None:
        """"Установить ширину"""

    @final
    def setSize(self, new_size: Vector2D[T]) -> None:
        """Установить размер"""
        self.setWidth(new_size.x)
        self.setHeight(new_size.y)


@dataclass(kw_only=True)
class Toggleable(ABC):
    """Объект, который может быть включен или выключен"""

    _enabled: bool = True
    """Объект включен"""

    @abstractmethod
    def setEnabled(self, enabled: bool) -> None:
        """Установить включенность объекта"""

    @abstractmethod
    def isEnabled(self) -> bool:
        """Включен объект"""

    @final
    def enable(self) -> None:
        """Включить"""
        self.setEnabled(True)

    @final
    def disable(self) -> None:
        """Отключить"""
        self.setEnabled(False)


@dataclass(kw_only=True)
class Visibility(ABC):
    """Способен управлять видимостью"""

    _visible: bool = True
    """Объект видимый"""

    @abstractmethod
    def setVisibility(self, is_visible: bool) -> None:
        """Установить видимость объекта"""

    @abstractmethod
    def isVisible(self) -> bool:
        """Объект видимый"""

    @final
    def show(self) -> None:
        """Показать"""
        self.setVisibility(True)

    @final
    def hide(self) -> None:
        """Скрыть"""
        self.setVisibility(False)


class Deletable(ABC):
    """Удаляемый объект"""

    @abstractmethod
    def delete(self) -> None:
        """Удалить"""
