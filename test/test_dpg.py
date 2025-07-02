from __future__ import annotations

from dpg_ui.core.app import App
from dpg_ui.impl.button import Button
from dpg_ui.impl.container.box import HBox
from dpg_ui.impl.container.window import Window
from dpg_ui.impl.display.text import DisplayText
from dpg_ui.impl.input.text import InputText
from dpg_ui.impl.slider.float_ import FloatSlider

__w = (
    Window("Text window")
    .add(DisplayText(_value_default="text"))
    .add(
        HBox()
        .add(Button("Button"))
        .add(Button("Button"))
    )
    .add(InputText("string", print))
    .add(FloatSlider("float", _value_default=0.123, _interval_max=10, _interval_min=-10))
    .add(Window("SHoo", _auto_size=False).add(Button("lol")))
)

App(__w).run("title", 1280, 720)
