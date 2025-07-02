from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from dearpygui import dearpygui as dpg

from dpg_ui.abc.widget import Widget
from dpg_ui.core.dpg.intervaled import DpgIntervaledValuedWidget


@dataclass
class FloatSlider(DpgIntervaledValuedWidget[float]):
    _label: str

    _on_change: Callable[[float], None] = None

    _display_after_comma: int = 2

    def register(self, parent: Widget) -> None:
        self._tag = dpg.add_slider_float(
            parent=parent.tag(),
            label=self._label,
            default_value=self._value_default,
            callback=None if self._on_change is None else lambda _: self._on_change(self.getValue()),
            format=f"%.{self._display_after_comma}f",
            max_value=self._interval_max,
            min_value=self._interval_min,
        )
