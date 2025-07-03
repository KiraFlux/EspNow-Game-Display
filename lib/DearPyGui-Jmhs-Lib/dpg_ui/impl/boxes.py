from __future__ import annotations

from dataclasses import dataclass
from typing import Callable
from typing import Optional

from dearpygui import dearpygui as dpg

from dpg_ui.abc.widget import Widget
from dpg_ui.core.dpg.intervaled import DpgIntervaledValuedWidget
from dpg_ui.core.dpg.tag import DpgTag
from dpg_ui.core.dpg.valued import DpgValuedWidget


@dataclass(kw_only=True)
class _TextBox(DpgValuedWidget[str]):
    """Окно текста"""

    _label: str
    """Наименование"""

    _readonly: bool
    """Поле только для ввода"""

    _on_change: Optional[Callable[[str], None]] = None
    """При изменении"""

    _width: int = 0
    """Ширина"""

    _on_enter: bool = False
    """Засчитывать изменение по Enter"""

    def register(self, parent: Widget) -> None:
        self._onRegister(dpg.add_input_text(
            parent=parent.tag(),
            label=self._label,
            default_value=self._value_default,
            readonly=self._readonly,
            width=self._width
        ))

        if self._readonly:
            return

        self.configure(
            on_enter=self._on_enter,
        )

        if self._on_change is None:
            return

        self.configure(
            callback=lambda _: self._on_change(self.getValue()),
        )


def TextInput(label: str, on_change: Callable[[str], None], *, on_enter: bool = False, default: str = None, width: int = 0):
    """Создать окно ввода текста"""
    return _TextBox(
        _label=label,
        _readonly=False,
        _on_change=on_change,
        _on_enter=on_enter,
        _value_default=default,
        _width=width
    )


def TextDisplay(label: str, *, default: str = None, width: int = 0):
    """Создать окно вывода текста"""
    return _TextBox(
        _label=label,
        _readonly=True,
        _on_change=None,
        _on_enter=False,
        _value_default=default,
        _width=width
    )


@dataclass(kw_only=True)
class _IntBox(DpgIntervaledValuedWidget[int]):
    """Окно целого числа"""

    label: str
    width: int = 0

    def register(self, parent: Widget) -> None:
        self._onRegister(dpg.add_input_int(
            parent=parent.tag(),
            label=self.label,
            default_value=self._value_default,
            width=self.width
        ))


class IntInput(_IntBox):
    """Окно ввода целого числа"""

    on_change: Optional[Callable[[int], None]] = None
    step: int = 1
    step_fast: int = 5

    def _onRegister(self, tag: DpgTag) -> None:
        super()._onRegister(tag)

        self.configure(
            readonly=False,
            step=self.step,
            step_fast=self.step_fast,
        )

        if self._interval_min is not None:
            self.configure(
                min_value=self._interval_min,
            )

        if self._interval_max is not None:
            self.configure(
                max_value=self._interval_max,
            )

        if self.on_change is not None:
            self.configure(callback=lambda _: self.on_change(self.getValue()))


class IntDisplay(_IntBox):
    """Окно отображения целого числа"""
