from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from dearpygui import dearpygui as dpg

from dpg_ui.abc.widget import Widget
from dpg_ui.core.dpg.intervaled import DpgIntervaledValuedWidget


@dataclass
class IntSlider(DpgIntervaledValuedWidget[int]):
    _label: str

    _on_change: Callable[[int], None] = None

    def register(self, parent: Widget) -> None:
        self._onRegister(dpg.add_slider_int(
            parent=parent.tag(),
            label=self._label,
            default_value=self._value_default,
            callback=None if self._on_change is None else lambda _: self._on_change(self.getValue()),
            max_value=self._interval_max,
            min_value=self._interval_min
        ))
