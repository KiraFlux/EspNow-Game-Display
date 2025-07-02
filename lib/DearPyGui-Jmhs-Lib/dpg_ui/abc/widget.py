from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import final


class Widget[T](ABC):
    """Виджет"""

    @abstractmethod
    def register(self, parent: Widget) -> None:
        """Зарегистрировать элемент"""

    @abstractmethod
    def tag(self) -> T:
        """Получить тег виджета"""

    @final
    def isRegistered(self) -> bool:
        """Виджет уже зарегистрирован"""
        return self.tag() is not None
