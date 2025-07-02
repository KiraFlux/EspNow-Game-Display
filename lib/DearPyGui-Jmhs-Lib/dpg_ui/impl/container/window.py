from __future__ import annotations

from dataclasses import dataclass

import dearpygui.dearpygui as dpg

from dpg_ui.abc.widget import Widget
from dpg_ui.core.dpg.container import DpgContainer


@dataclass
class Window(DpgContainer):
    """Окно"""

    _label: str
    """Заголовок окна"""

    _menubar: bool = False
    """Место под полосу меню"""

    _auto_size: bool = True
    """Размер окна автоматически подстраивается под виджеты"""

    def register(self, parent: Widget) -> None:
        self._tag = dpg.add_window(
            label=self._label,
            menubar=self._menubar,
            autosize=self._auto_size,
        )

        self._registerItems()
