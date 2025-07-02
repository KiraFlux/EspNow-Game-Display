from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import MutableSequence
from typing import Self

from dearpygui import dearpygui as dpg

from dpg_ui.abc.container import Container
from dpg_ui.abc.widget import Widget
from dpg_ui.core.dpg.item import DpgWidget


@dataclass
class Window(DpgWidget, Container):
    """Окно"""

    _label: str
    """Заголовок окна"""

    _menubar: bool = False
    """Место под полосу меню"""

    _auto_size: bool = True
    """Размер окна автоматически подстраивается под виджеты"""

    _items: MutableSequence[Widget] = field(init=False, default_factory=list)

    def render(self, parent: Widget) -> None:
        self._tag = dpg.add_window(
            label=self._label,
            menubar=self._menubar,
            autosize=self._auto_size,

        )

        for item in self._items:
            item.render(self)

    def add(self, item: Widget) -> Self:
        self._items.append(item)
        return self
