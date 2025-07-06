from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from typing import Callable
from typing import Optional
from typing import final

from dearpygui import dearpygui as dpg

from dpg_ui.core.dpg.item import DpgTag
from dpg_ui.core.dpg.traits import DpgIntervaled
from dpg_ui.core.dpg.traits import DpgSizable
from dpg_ui.core.dpg.traits import DpgValued
from dpg_ui.core.dpg.traits import DpgWidthAdjustable
from dpg_ui.core.dpg.widget import DpgWidget


@dataclass(kw_only=True)
class _InputBox[T](DpgWidget, DpgValued[T], DpgWidthAdjustable[int], ABC):
    """Окно значения"""

    _label: Optional[str]
    """Наименование"""

    _readonly: bool
    """Поле только для ввода"""

    _on_change: Optional[Callable[[T], None]]
    """При изменении"""

    _on_enter: bool
    """Засчитывать изменение по Enter"""

    def _onRegister(self, tag: DpgTag) -> None:
        super()._onRegister(tag)

        self._updateWidth()
        self._updateValue()


@final
@dataclass(kw_only=True)
class _InputText(_InputBox[str], DpgSizable[int]):
    """Окно текста"""

    def _onRegister(self, tag: DpgTag) -> None:
        super()._onRegister(tag)
        self._updateHeight()

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_input_text(
            parent=parent_tag,
            label=self._label,
            readonly=self._readonly,

            on_enter=self._on_enter,
            callback=None if self._on_change is None else (lambda _: self._on_change(self.getValue()))
        )


def InputText(
        label: str,
        on_change: Callable[[str], None],
        *,
        on_enter: bool = False,
        default: str = None,
):
    """Создать окно ввода текста"""
    return _InputText(
        _label=label,
        _readonly=False,
        _on_change=on_change,
        _on_enter=on_enter,
        _value=default,
    )


def DisplayText(
        label: str,
        *,
        default: str = None,
):
    """Создать окно вывода текста"""
    return _InputText(
        _label=label,
        _readonly=True,
        _on_change=None,
        _on_enter=False,
        _value=default,
    )


@final
@dataclass(kw_only=True)
class _InputInt(_InputBox[int], DpgIntervaled[int]):
    """Окно целого числа"""

    _step: int

    _step_fast: int

    def _onRegister(self, tag: DpgTag) -> None:
        super()._onRegister(tag)

        self._updateIntervalMax()
        self._updateIntervalMin()

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        clamped = self._interval_min != self._interval_max

        return dpg.add_input_int(
            parent=parent_tag,

            label=self._label,
            readonly=self._readonly,
            callback=None if self._on_change is None else (lambda _: self._on_change(self.getValue())),

            step_fast=self._step_fast,
            step=self._step,

            min_clamped=clamped,
            max_clamped=clamped,
        )


def InputInt(
        label: Optional[str],
        on_change: Callable[[int], None] = None,
        default: int = 0,
        *,
        step: int = 1,
        step_fast: int = 1,
        interval_min: int = 0,
        interval_max: int = 0,
        on_enter: bool = False,
):
    """Окно ввода целого числа"""
    return _InputInt(
        _interval_max=interval_max,
        _interval_min=interval_min,
        _value=default,
        _label=label,
        _readonly=False,
        _on_change=on_change,
        _on_enter=on_enter,
        _step=step,
        _step_fast=step_fast,
    )


def DisplayInt(
        label: str,
        *,
        default: int = 0,
):
    """Окно вывода целого числа"""
    return _InputInt(
        _interval_max=0,
        _interval_min=0,

        _value=default,
        _label=label,
        _readonly=True,
        _on_change=None,
        _on_enter=False,

        _step=0,
        _step_fast=0
    )
