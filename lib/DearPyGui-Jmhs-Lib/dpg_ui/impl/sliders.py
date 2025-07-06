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
class _Slider[T](DpgWidget, DpgValued[T], DpgIntervaled[T], ABC):
    """Общий слайдер"""

    _label: str
    """Описание"""

    _on_change: Optional[Callable[[T], None]]
    """Обработчик при изменении значения"""

    _units: Optional[str]
    """Единицы измерения"""


@final
@dataclass
class _IntSlider(_Slider[int]):
    """Dpg: slider_int"""

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        f = "%d"

        if self._units:
            f = f"{f} {self._units}"

        return dpg.add_slider_int(
            parent=parent_tag,
            label=self._label,
            default_value=self._value,
            callback=None if self._on_change is None else lambda _: self._on_change(self.getValue()),
            max_value=self._interval_max,
            min_value=self._interval_min,
            format=f
        )


def IntSlider(
        label: str,
        *,
        default: int = 0,
        on_change: Callable[[int], None] = None,
        units: str = None,
        interval: tuple[int, int],

):
    """Целочисленный слайдер"""
    _min, _max = interval
    return _IntSlider(
        _interval_max=_max,
        _interval_min=_min,
        _value=default,
        _label=label,
        _on_change=on_change,
        _units=units,
    )


@final
@dataclass
class _FloatSlider(_Slider[float]):
    """Dpg: slider_float"""

    _digits_after_comma: int
    """Цифр после запятой"""

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        f = f"%.{self._digits_after_comma}f"

        if self._units:
            f = f"{f} {self._units}"

        return dpg.add_slider_float(
            parent=parent_tag,
            label=self._label,
            default_value=self._value,
            callback=None if self._on_change is None else lambda _: self._on_change(self.getValue()),
            format=f,
            max_value=self._interval_max,
            min_value=self._interval_min,
        )


def FloatSlider(
        label: str,
        *,
        default: float = 0,
        on_change: Callable[[float], None] = None,
        units: str = None,
        interval: tuple[float, float],
        digits: int = 2,

):
    """Вещественный слайдер"""
    _min, _max = interval
    return _FloatSlider(
        _interval_max=_max,
        _interval_min=_min,
        _value=default,
        _label=label,
        _on_change=on_change,
        _units=units,
        _digits_after_comma=digits
    )
