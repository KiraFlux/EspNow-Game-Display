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
        self._onRegister(dpg.add_window(
            label=self._label,
            menubar=self._menubar,
            autosize=self._auto_size,
        ))


@dataclass(kw_only=True)
class ChildWindow(DpgContainer):
    """Дочернее очно"""

    # Основные параметры
    width: int = 0
    height: int = 0

    resizable_x: bool = False
    resizable_y: bool = False

    # Внешний вид
    border: bool = True
    background: bool = False
    menu_bar: bool = False

    scrollable_y: bool = True
    scrollable_x: bool = False

    def register(self, parent: Widget) -> None:
        # Автоматическое разрешение конфликтов

        self._onRegister(dpg.add_child_window(
            parent=parent.tag(),
            border=self.border,
            frame_style=self.background,
            menubar=self.menu_bar,
            resizable_x=self.resizable_x,
            resizable_y=self.resizable_y,
            no_scrollbar=not self.scrollable_y,
            horizontal_scrollbar=self.scrollable_x,
        ))

        if self.width > 0:
            self.configure(width=self.width)

        if self.height > 0:
            self.configure(height=self.height)
