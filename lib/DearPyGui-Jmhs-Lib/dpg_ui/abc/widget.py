from __future__ import annotations

from abc import ABC
from abc import abstractmethod


class Widget[T](ABC):
    """Виджет"""

    @abstractmethod
    def render(self, parent: Widget) -> None:
        """Отобразить элемент"""

    @abstractmethod
    def tag(self) -> T:
        """Получить тег виджета"""
