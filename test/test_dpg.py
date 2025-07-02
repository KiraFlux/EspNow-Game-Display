from __future__ import annotations

import dearpygui.dearpygui as dpg

from dpg_ui.impl.widget.text import Text
from dpg_ui.impl.window import Window

dpg.create_context()
dpg.create_viewport(title='Custom Title', width=600, height=300)

window = Window("Text window")
text = Text("Text")

(
    window
    .add(text)

).render(None)

dpg.add_button(label="Save", parent=window.tag(), callback=lambda _: text.setValue(str(_)))

dpg.add_input_text(label="string", default_value="Quick brown fox", parent=window.tag())

dpg.add_slider_float(label="float", default_value=0.273, max_value=1, parent=window.tag())

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
