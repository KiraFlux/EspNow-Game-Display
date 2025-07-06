from __future__ import annotations

from dataclasses import dataclass
from typing import final

from dearpygui import dearpygui as dpg

from dpg_ui.core.dpg.item import DpgTag
from dpg_ui.core.dpg.traits import DpgColored
from dpg_ui.core.dpg.traits import DpgValued
from dpg_ui.core.dpg.widget import DpgWidget
from rs.color import Color


@final
@dataclass
class _Text(DpgWidget, DpgValued[str], DpgColored):
    """Текст"""

    _bullet: bool = False
    """Отображает маркер перед текстом"""

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        tag = dpg.add_text(self._value, parent=parent_tag, color=self._color.toRGBA8888(), bullet=self._bullet, )
        return tag


def Text(
        default: str = None,
        *,
        color: Color = Color.white(),
        bullet: bool = False
):
    """Текст"""
    return _Text(_bullet=bullet, _value=default, _color=color)
