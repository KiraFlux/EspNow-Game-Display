from __future__ import annotations

from dpg_ui.core.app import App
from dpg_ui.core.custom import CustomWidget
from dpg_ui.impl.containers import Window
from dpg_ui.impl.text import Text


class Foo(CustomWidget):

    def __init__(self) -> None:
        super().__init__(Text("LOL"))


w = Window("")

foo = Foo()
w.add(
    foo
)

#
App(w).run("title", 1280, 720)
