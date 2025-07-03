from __future__ import annotations

from dataclasses import dataclass
from typing import Callable
from typing import Optional

from dearpygui import dearpygui as dpg

from dpg_ui.abc.widget import Widget
from dpg_ui.core.dpg.valued import DpgValuedWidget

type cb = Callable[[str], None]


@dataclass(kw_only=True)
class _TextBox(DpgValuedWidget[str]):
    """Окно текста"""

    _label: str
    """Наименование"""

    _readonly: bool
    """Поле только для ввода"""

    _on_change: Optional[cb] = None
    """При изменении"""

    _on_enter: bool = False
    """Засчитывать изменение по Enter"""

    def register(self, parent: Widget) -> None:
        self._onRegister(dpg.add_input_text(
            label=self._label,
            default_value=self._value_default,
            parent=parent.tag(),
            callback=None if self._on_change is None else (lambda _: self._on_change(self.getValue())),
            on_enter=self._on_enter,
            readonly=self._readonly
        ))


def TextInput(label: str, on_change: cb, *, on_enter: bool = False, default: str = None):
    """Создать окно ввода текста"""
    return _TextBox(
        _label=label,
        _readonly=False,
        _on_change=on_change,
        _on_enter=on_enter,
        _value_default=default
    )


def TextDisplay(label: str, *, default: str = None):
    """Создать окно вывода текста"""
    return _TextBox(
        _label=label,
        _readonly=True,
        _on_change=None,
        _on_enter=False,
        _value_default=default
    )
