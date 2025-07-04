from __future__ import annotations

from abc import ABC
from typing import final

from dearpygui import dearpygui as dpg

from dpg_ui.abc.traits import Colored
from dpg_ui.abc.traits import Deletable
from dpg_ui.abc.traits import Enableable
from dpg_ui.abc.traits import Intervaled
from dpg_ui.abc.traits import Valued
from dpg_ui.abc.traits import Visibility
from dpg_ui.core.dpg.item import DpgItem
from rs.color import Color


class DpgColored(DpgItem, Colored):
    @final
    def _setColorImpl(self, color: Color) -> None:
        self.configure(color=color.toRGBA8888())


class DpgEnableable(DpgItem, Enableable):
    @final
    def disable(self) -> None:
        dpg.disable_item(self.tag())

    @final
    def enable(self) -> None:
        dpg.enable_item(self.tag())


class DpgDeletable(DpgItem, Deletable):
    @final
    def delete(self) -> None:
        dpg.delete_item(self.tag())


class DpgVisibility(DpgItem, Visibility):
    @final
    def hide(self) -> None:
        if self.isRegistered():
            dpg.hide_item(self.tag())

    @final
    def show(self) -> None:
        if self.isRegistered():
            dpg.show_item(self.tag())


class DpgValued[T](DpgItem, Valued[T], ABC):
    """Виджет со значением на стороне DPG"""

    @final
    def getValue(self) -> T:
        if self.isRegistered():
            return dpg.get_value(self.tag())

        else:
            return self._value_default

    @final
    def setValue(self, value: T) -> None:
        if self.isRegistered():
            dpg.set_value(self.tag(), value)

        else:
            self._value_default = value


class DpgIntervaled[T](DpgItem, Intervaled[T], ABC):
    """Виджет DPG имеет диапазон и значение"""

    def _onIntervalMaxChanged(self, new_max: T) -> None:
        self.configure(max_value=new_max)

    def _onIntervalMinChanged(self, new_min: T) -> None:
        self.configure(min_value=new_min)
