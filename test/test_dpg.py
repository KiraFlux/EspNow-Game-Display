from __future__ import annotations

from dpg_ui.core.app import App
from dpg_ui.impl.button import Button
from dpg_ui.impl.container.box import HBox
from dpg_ui.impl.container.tab import Tab
from dpg_ui.impl.container.tab import TabBar
from dpg_ui.impl.container.window import Window
from dpg_ui.impl.display.text import DisplayText
from dpg_ui.impl.input.text import InputText
from dpg_ui.impl.slider.float_ import FloatSlider

tab_bar = (
    TabBar(_reorderable=True)
    .add(
        Tab("Tab 1")
        .add(
            HBox()
            .add(Button("Button"))
            .add(Button("1234567"))
        )
    )
    .add(
        Tab("2")
        .add(InputText("string", print))
        .add(FloatSlider("float", _value_default=0.123, _interval_max=10, _interval_min=-10))
    )
)

__w = (
    Window("Text window")
    .add(
        HBox()
        .add(tab_bar)
        .add(DisplayText(_value_default="text"))
    )
    .add(
        Window("SHoo", _auto_size=False)
        .add(Button("lol"))
    )
)

App(__w).run("title", 1280, 720)
