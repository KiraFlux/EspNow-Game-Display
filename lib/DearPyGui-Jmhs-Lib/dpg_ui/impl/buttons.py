from dataclasses import dataclass
from dataclasses import field
from typing import Callable
from typing import final

from dearpygui import dearpygui as dpg

from dpg_ui.core.dpg.item import DpgTag
from dpg_ui.core.dpg.traits import DpgValued
from dpg_ui.core.dpg.widget import DpgWidget
from rs.color import Color


@dataclass
class _Button(DpgWidget):
    _label: str
    """Надпись"""

    _on_click: Callable[[], None] = field(kw_only=True, default=None)
    """Callback"""

    _width: int = field(kw_only=True, default=0)
    """Ширина"""

    _height: int = field(kw_only=True, default=0)
    """Высота"""


@final
@dataclass
class Button(_Button):
    """Dpg: button"""

    _small: bool = field(kw_only=True, default=False)
    """Меньший размер кнопки"""

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_button(
            parent=parent_tag,

            label=self._label,
            callback=None if self._on_click is None else (lambda _: self._on_click()),
            width=self._width,
            height=self._height,

            small=self._small,
        )


@dataclass
class ColorDisplay(_Button):
    """Кнопка"""

    _color: Color
    _border: bool = field(kw_only=True, default=False)

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_color_button(
            parent=parent_tag,

            label=self._label,
            callback=None if self._on_click is None else (lambda _: self._on_click()),
            width=self._width,
            height=self._height,

            no_border=not self._border,
            default_value=self._color.toRGBA8888(),
        )


@final
@dataclass
class CheckBox(DpgWidget, DpgValued[bool]):
    """Dpg: checkbox"""

    _label: str

    _on_change: Callable[[bool], None] = None

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_checkbox(
            parent=parent_tag,
            label=self._label,
            default_value=bool(self._value_default),
            callback=None if self._on_change is None else (lambda _: self._on_change(self.getValue()))
        )
