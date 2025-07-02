from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

from dearpygui import dearpygui as dpg

from dpg_ui.abc.widget import Widget
from dpg_ui.core.dpg.valued import DpgValuedWidget


@dataclass
class InputText(DpgValuedWidget[str]):
    """Ввод текста"""

    _label: str

    _on_change: Callable[[str], None] = None

    _on_enter: bool = False

    def register(self, parent: Widget) -> None:
        self._onRegister(dpg.add_input_text(
            label=self._label,
            default_value=self._value_default,
            parent=parent.tag(),
            callback=None if self._on_change is None else (lambda _: self._on_change(self.getValue())),
            on_enter=self._on_enter
        ))
