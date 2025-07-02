"""Компонент интерфейса для цвета"""

from __future__ import annotations

from dataclasses import dataclass

from dearpygui import dearpygui as dpg

from dpg_ui.abc.colored import Colored
from dpg_ui.abc.valued import Valued
from dpg_ui.abc.widget import Widget
from dpg_ui.core.dpg.item import DpgWidget
from rs.color import Color


@dataclass
class Text(Colored, Valued[str], DpgWidget):
    """Текст"""

    _bullet: bool = False
    """Отображает маркер перед текстом"""

    def _setColorImpl(self, color: Color) -> None:
        self.configure(color=color.toRGBA8888())

    def getValue(self) -> str:
        return dpg.get_value(self.tag())

    def setValue(self, value: str) -> None:
        dpg.set_value(self.tag(), value)

    def render(self, parent: Widget) -> None:
        self._tag = dpg.add_text(
            self._default_value,
            parent=parent.tag(),
            color=self._color.toRGBA8888(),
            bullet=self._bullet,
        )
