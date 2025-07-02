from __future__ import annotations

import dearpygui.dearpygui as dpg

from dpg_ui.impl.widget.button import Button
from dpg_ui.impl.widget.text import Text
from dpg_ui.impl.window import Window

dpg.create_context()
dpg.create_viewport(title='Custom Title', width=600, height=300)

__w = Window("Text window")
text = Text("Text")

(
    __w
    .add(text)
    .add(Button("Button"))
    .add(Button("Button"))
).render(None)

dpg.add_input_text(label="string", default_value="Quick brown fox", parent=__w.tag())

dpg.add_slider_float(label="float", default_value=0.273, max_value=1, parent=__w.tag())

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
