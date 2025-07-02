from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import dearpygui.dearpygui as dpg

from dpg_ui.abc.widget import Widget
from dpg_ui.core.dpg.ranged import DpgRangedValuedWidget
from dpg_ui.impl.button import Button
from dpg_ui.impl.display.text import DisplayText
from dpg_ui.impl.input.text import InputText
from dpg_ui.impl.window import Window


@dataclass
class FloatSlider(DpgRangedValuedWidget[float]):
    _label: str

    _on_change: Callable[[float], None] = None

    _display_after_comma: int = 4

    def render(self, parent: Widget) -> None:
        self._tag = dpg.add_slider_float(
            label=self._label,
            default_value=self._value_default,
            parent=parent.tag(),
            callback=None if self._on_change is None else lambda _: self._on_change(self.getValue()),
            format=f"%.{self._display_after_comma}f",
            max_value=self._range_max,
            min_value=self._range_min,
        )


dpg.create_context()
dpg.create_viewport(title='Custom Title', width=600, height=300)

(
    Window("Text window")
    .add(DisplayText(_value_default="text"))
    .add(Button("Button"))
    .add(Button("Button"))
    .add(InputText("string", print))
    .add(FloatSlider("float", _value_default=0.123, _range_max=10, _range_min=-10))
).render(None)

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
