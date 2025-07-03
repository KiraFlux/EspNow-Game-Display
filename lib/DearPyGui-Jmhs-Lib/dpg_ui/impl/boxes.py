from __future__ import annotations

from dataclasses import dataclass
from typing import Callable
from typing import Optional

from dearpygui import dearpygui as dpg

from dpg_ui.abc.widget import Widget
from dpg_ui.core.dpg.intervaled import DpgIntervaledValuedWidget
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

    readonly: bool

    width: Optional[int]

    on_change: Optional[Callable[[int], None]]

    step: Optional[int]
    step_fast: Optional[int]

    def register(self, parent: Widget) -> None:
        self._onRegister(dpg.add_input_int(
            parent=parent.tag(),
            label=self.label,
            default_value=self._value_default,
            readonly=self.readonly,
        ))

        if self.width:
            self.configure(width=self.width)

        if self._interval_min:
            self.configure(min_value=self._interval_min)

        if self._interval_max:
            self.configure(max_value=self._interval_max)

        if self.on_change:
            self.configure(callback=lambda _: self.on_change(self.getValue()))

        if self.step:
            self.configure(step=self.step)

        if self.step_fast:
            self.configure(step_fast=self.step_fast)


def IntInput(
        label: str,
        on_change: Callable[[int], None] = None,
        default: int = 0,
        *,
        width: int = None,
        step: int = None,
        step_fast: int = None,
        interval_max: int = None,
        interval_min: int = None,
):
    """Окно ввода целого числа"""
    return _IntBox(
        _interval_min=interval_min,
        _interval_max=interval_max,
        _value_default=default,
        label=label,
        readonly=False,
        width=width,
        on_change=on_change,
        step=step,
        step_fast=step_fast,
    )


def IntDisplay(
        label: str,
        default: int = 0,
        *,
        width: int = None
):
    """Окно вывода целого числа"""
    return _IntBox(
        readonly=True,
        width=width,
        on_change=None,
        step=None,
        step_fast=None,
        _value_default=default,
        label=label,
    )
