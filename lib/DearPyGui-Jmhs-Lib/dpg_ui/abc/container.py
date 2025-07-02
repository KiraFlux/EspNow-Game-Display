from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Self

from dpg_ui.abc.widget import Widget


class Container(ABC):
    """Способен содержат другие виджеты"""

    @abstractmethod
    def add(self, item: Widget) -> Self:
        """Добавить дочерний элемент"""
