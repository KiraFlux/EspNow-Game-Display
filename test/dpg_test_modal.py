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

w = (
    Window()
    .add(
        ComboBox()
        .withWidth(100)
        .withHandler(lambda x: print(x))
        .add(1)
        .add(2)
        .add(3)
    )
    .add(
        Button()
        .withLabel("Show modal")
        .withWidth(100)
        .withHandler(modal.show)
    )
    .add(
        Text(str(globals()))
    )
)

App(w).run("Test", 1280, 720)
