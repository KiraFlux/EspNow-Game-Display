from abc import ABC
from dataclasses import dataclass
from dataclasses import field
from typing import Callable
from typing import final

from dearpygui import dearpygui as dpg

from dpg_ui.core.dpg.item import DpgTag
from dpg_ui.core.dpg.traits import DpgColored
from dpg_ui.core.dpg.traits import DpgSizable
from dpg_ui.core.dpg.traits import DpgValued
from dpg_ui.core.dpg.widget import DpgWidget


@dataclass
class _Button(DpgWidget, DpgSizable, ABC):
    _label: str
    """Надпись"""

    _on_click: Callable[[], None] = field(kw_only=True, default=None)
    """Callback"""

    def _onRegister(self, tag: DpgTag) -> None:
        super()._onRegister(tag)

        self._updateWidth()
        self._updateHeight()


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

            small=self._small,
        )


@dataclass
class ColorDisplay(_Button, DpgColored):
    """Кнопка"""

    _border: bool = field(kw_only=True, default=False)

    def _updateColor(self):
        self.configure(default_value=self._color.toRGBA8888())

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_color_button(
            parent=parent_tag,

            label=self._label,
            callback=None if self._on_click is None else (lambda _: self._on_click()),

            no_border=not self._border,
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
            default_value=bool(self._value),
            callback=None if self._on_change is None else (lambda _: self._on_change(self.getValue()))
        )
