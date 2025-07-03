from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Self
from typing import final

from dpg_ui.abc.font import Font
from dpg_ui.abc.item import Item


class Widget[T](Item[T], ABC):
    """Виджет"""

    @abstractmethod
    def register(self, parent: Widget) -> None:
        """Зарегистрировать элемент"""

    @abstractmethod
    def withFont(self, font: Font) -> Self:
        """Установить шрифт"""

    @abstractmethod
    def enable(self) -> None:
        """Включить"""

    @abstractmethod
    def disable(self) -> None:
        """Отключить"""

    @final
    def setEnabled(self, is_enabled: bool) -> None:
        """Установить включенность объекта"""

        if is_enabled:
            self.enable()
        else:
            self.disable()

    @abstractmethod
    def show(self) -> None:
        """Показать"""

    @abstractmethod
    def hide(self) -> None:
        """Скрыть"""

    @final
    def setVisibility(self, is_visible: bool) -> None:
        """Установить видимость объекта"""

        if is_visible:
            self.show()
        else:
            self.hide()

    @abstractmethod
    def delete(self) -> None:
        """Удалить"""
