from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from typing import final

from rs.color import Color


@dataclass(kw_only=True)
class Colored(ABC):
    """Содержит цвет"""

    _color: Color
    """Цвет"""

    @abstractmethod
    def _setColorImpl(self, color: Color) -> None:
        """Реализация изменения цвета """

    @final
    def setColor(self, color: Color) -> None:
        """Изменить цвет"""
        self._color = color
        self._setColorImpl(color)

    @final
    def getColor(self) -> Color:
        """Получить актуальный цвет"""
        return self._color
