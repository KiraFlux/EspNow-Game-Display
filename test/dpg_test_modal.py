from dpg_ui.core.app import App
from dpg_ui.impl.buttons import Button
from dpg_ui.impl.containers import ComboBox
from dpg_ui.impl.containers import Window
from dpg_ui.impl.text import Text

modal = (
    Window(
        _auto_size=True,
        _modal=True,
        _visible=False,
    )
    .withWidth(900)
    .withLabel("Modal")
)

combo = ComboBox(_items_provider=(lambda: (1, 2, 3)), _value=1).withWidth(100)

w = (
    Window()
    .add(
        combo
    )
    .add(
        Button()
        .withLabel("Show modal")
        .withWidth(100)
        .withHandler(lambda: print(repr(combo.getValue())))
    )
    .add(
        Text(str(globals()))
    )
)

App(w).run("Test", 1280, 720)
