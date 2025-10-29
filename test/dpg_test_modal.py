from kf_dpg.core.app import App
from kf_dpg.impl.buttons import Button
from kf_dpg.impl.containers import ComboBox
from kf_dpg.impl.containers import Window
from kf_dpg.impl.text import Text

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
