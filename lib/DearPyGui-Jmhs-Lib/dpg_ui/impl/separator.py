import dearpygui.dearpygui as dpg

from dpg_ui.abc.widget import Widget
from dpg_ui.core.dpg.widget import DpgWidget


class Separator(DpgWidget):
    """Разделитель"""

    def register(self, parent: Widget) -> None:
        self._onRegister(dpg.add_separator(
            parent=parent.tag()
        ))
