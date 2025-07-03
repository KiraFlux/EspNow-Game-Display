from dataclasses import dataclass
from typing import Callable

import dearpygui.dearpygui as dpg

from dpg_ui.abc.widget import Widget
from dpg_ui.core.dpg.valued import DpgValuedWidget


@dataclass
class CheckBox(DpgValuedWidget[bool]):
    """Check box"""

    label: str

    on_change: Callable[[bool], None] = None

    def register(self, parent: Widget) -> None:
        self._onRegister(dpg.add_checkbox(
            label=self.label,
            parent=parent.tag(),
            default_value=bool(self._value_default),
            callback=None if self.on_change is None else (lambda _: self.on_change(self.getValue()))
        ))
