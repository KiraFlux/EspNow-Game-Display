from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Self

from dpg_ui.abc.font import Font
from dpg_ui.abc.item import Item


class Widget[T](Item[T], ABC):
    """Виджет"""

    @abstractmethod
    def register(self, parent: Widget) -> None:
        """Зарегистрировать элемент"""

    @abstractmethod
    def setFont(self, font: Font) -> Self:
        """Установить шрифт"""
