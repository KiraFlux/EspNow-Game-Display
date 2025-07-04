from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from typing import Callable
from typing import Optional
from typing import final

from dearpygui import dearpygui as dpg

from dpg_ui.core.dpg.item import DpgTag
from dpg_ui.core.dpg.traits import DpgIntervaled
from dpg_ui.core.dpg.traits import DpgValued
from dpg_ui.core.dpg.widget import DpgWidget


@dataclass(kw_only=True)
class _ValueBox[T](DpgWidget, DpgValued[T], ABC):
    """Окно значения"""

    _label: str
    """Наименование"""

    _readonly: bool
    """Поле только для ввода"""

    _on_change: Optional[Callable[[T], None]]
    """При изменении"""

    _width: int
    """Ширина"""

    _on_enter: bool
    """Засчитывать изменение по Enter"""


@final
@dataclass(kw_only=True)
class _TextBox(_ValueBox[str]):
    """Окно текста"""

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_input_text(
            parent=parent_tag,
            label=self._label,
            default_value=self._value_default,
            readonly=self._readonly,
            width=self._width,
            on_enter=self._on_enter,
            callback=None if self._on_change is None else (lambda _: self._on_change(self.getValue()))
        )


def TextInput(
        label: str,
        on_change: Callable[[str], None],
        *,
        on_enter: bool = False,
        default: str = None,
        width: int = 0
):
    """Создать окно ввода текста"""
    return _TextBox(
        _label=label,
        _readonly=False,
        _on_change=on_change,
        _on_enter=on_enter,
        _value_default=default,
        _width=width
    )


def TextDisplay(
        label: str,
        *,
        default: str = None,
        width: int = 0
):
    """Создать окно вывода текста"""
    return _TextBox(
        _label=label,
        _readonly=True,
        _on_change=None,
        _on_enter=False,
        _value_default=default,
        _width=width
    )


@final
@dataclass(kw_only=True)
class _IntInputBox(_ValueBox[int], DpgIntervaled[int]):
    """Окно целого числа"""

    _step: int

    _step_fast: int

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_input_int(
            parent=parent_tag,

            label=self._label,
            default_value=self._value_default,
            readonly=self._readonly,
            width=self._width,
            callback=None if self._on_change is None else (lambda _: self._on_change(self.getValue())),

            max_value=self._interval_max,
            min_value=self._interval_min,

            step_fast=self._step_fast,
            step=self._step,
        )


def IntInput(
        label: str,
        on_change: Callable[[int], None] = None,
        default: int = 0,
        *,
        width: int = 0,
        step: int = 1,
        step_fast: int = 1,
        interval_min: int = 0,
        interval_max: int = 0,
        on_enter: bool = False,
):
    """Окно ввода целого числа"""
    return _IntInputBox(
        _interval_max=interval_max,
        _interval_min=interval_min,
        _value_default=default,
        _label=label,
        _readonly=False,
        _on_change=on_change,
        _width=width,
        _on_enter=on_enter,
        _step=step,
        _step_fast=step_fast,
    )


def IntDisplay(
        label: str,
        default: int = 0,
        *,
        width: int = 0
):
    """Окно вывода целого числа"""
    return _IntInputBox(
        _interval_max=0,
        _interval_min=0,
        _value_default=default,
        _label=label,
        _readonly=True,
        _on_change=None,
        _width=width,
        _on_enter=False,
        _step=0,
        _step_fast=0
    )
