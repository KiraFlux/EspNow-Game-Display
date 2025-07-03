from dataclasses import dataclass
from typing import Callable

from dearpygui import dearpygui as dpg

from dpg_ui.abc.widget import Widget
from dpg_ui.core.dpg.widget import DpgWidget


@dataclass
class Button(DpgWidget):
    """Кнопка"""

    _label: str
    """Надпись"""

    _on_click: Callable[[], None] = None
    """Callback"""

    _small: bool = False
    """Меньший размер кнопки"""

    def register(self, parent: Widget) -> None:
        self._onRegister(dpg.add_button(
            label=self._label,
            parent=parent.tag(),
            small=self._small,
            callback=None if self._on_click is None else (lambda _: self._on_click())
        ))
