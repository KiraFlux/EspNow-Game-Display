"""Компонент интерфейса для цвета"""

from __future__ import annotations

from dataclasses import dataclass

from dearpygui import dearpygui as dpg

from dpg_ui.abc.colored import Colored
from dpg_ui.abc.widget import Widget
from dpg_ui.core.dpg.valued import DpgValuedWidget
from rs.color import Color


@dataclass
class _Text(Colored, DpgValuedWidget[str]):
    """Текст"""

    _bullet: bool = False
    """Отображает маркер перед текстом"""

    def _setColorImpl(self, color: Color) -> None:
        self.configure(color=color.toRGBA8888())

    def register(self, parent: Widget) -> None:
        self._onRegister(dpg.add_text(
            self._value_default,
            parent=parent.tag(),
            color=self._color.toRGBA8888(),
            bullet=self._bullet,
        ))


def Text(
        default: str = None,
        *,
        color: Color = Color.white(),
        bullet: bool = False
):
    """Текст"""
    return _Text(
        _bullet=bullet,
        _value_default=default,
        _color=color
    )
