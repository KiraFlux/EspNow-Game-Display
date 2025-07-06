from __future__ import annotations

from abc import ABC
from typing import final

from dearpygui import dearpygui as dpg

from dpg_ui.abc.traits import Colored
from dpg_ui.abc.traits import Deletable
from dpg_ui.abc.traits import Intervaled
from dpg_ui.abc.traits import Sizable
from dpg_ui.abc.traits import Toggleable
from dpg_ui.abc.traits import Valued
from dpg_ui.abc.traits import Visibility
from dpg_ui.abc.traits import WidthAdjustable
from dpg_ui.core.dpg.item import DpgItem
from rs.color import Color


class DpgColored(DpgItem, Colored):
    @final
    def setColor(self, color: Color) -> None:
        self._color = color

        if self.isRegistered():
            self._updateColor()

    def _updateColor(self):
        self.configure(color=super().getColor().toRGBA8888())


class DpgToggleable(DpgItem, Toggleable):
    @final
    def isEnabled(self) -> bool:
        if self.isRegistered():
            self._enabled = dpg.is_item_enabled(self.tag())

        return self._enabled

    @final
    def setEnabled(self, enabled: bool) -> None:
        self._enabled = enabled

        if self.isRegistered():
            self._updateEnabled()

    @final
    def _updateEnabled(self) -> None:
        if self._enabled:
            dpg.enable_item(self.tag())
        else:
            dpg.disable_item(self.tag())


class DpgDeletable(DpgItem, Deletable):
    @final
    def delete(self) -> None:
        dpg.delete_item(self.tag())


class DpgVisibility(DpgItem, Visibility):
    @final
    def isVisible(self) -> bool:
        if self.isRegistered():
            self._visible = dpg.is_item_visible(self.tag())

        return self._visible

    @final
    def setVisibility(self, is_visible: bool) -> None:
        self._visible = is_visible

        if self.isRegistered():
            self._updateVisibility()

    @final
    def _updateVisibility(self) -> None:
        if self._visible:
            dpg.show_item(self.tag())
        else:
            dpg.hide_item(self.tag())


class DpgValued[T](DpgItem, Valued[T], ABC):
    """Виджет со значением на стороне DPG"""

    @final
    def getValue(self) -> T:
        if self.isRegistered():
            self._value = dpg.get_value(self.tag())

        return self._value

    @final
    def setValue(self, value: T) -> None:
        self._value = value

        if self.isRegistered():
            self._updateValue()

    @final
    def _updateValue(self):
        dpg.set_value(self.tag(), self._value)


class DpgIntervaled[T](DpgItem, Intervaled[T]):
    """Виджет DPG имеющий диапазон и значение"""

    @final
    def setIntervalMax(self, new_max: T) -> None:
        self._interval_max = new_max

        if self.isRegistered():
            self._updateIntervalMax()

    def setIntervalMin(self, new_min: T) -> None:
        self._interval_min = new_min

        if self.isRegistered():
            self._updateIntervalMin()

    @final
    def _updateIntervalMax(self) -> None:
        self.configure(max_value=self._interval_max)

    @final
    def _updateIntervalMin(self) -> None:
        self.configure(min_value=self._interval_min)


class DpgWidthAdjustable[T: (int, float)](DpgItem, WidthAdjustable[T]):
    """Объект DPG способный управлять шириной"""

    @final
    def setWidth(self, width: T) -> None:
        self._width = width

        if self.isRegistered():
            self._updateWidth()

    @final
    def getWidth(self) -> T:
        if self.isRegistered():
            self._width = dpg.get_item_width(self.tag())

        return self._width

    @final
    def _updateWidth(self) -> None:
        self.configure(width=self._width)


class DpgSizable[T: (int, float)](Sizable[T], DpgWidthAdjustable[T], DpgItem):
    """Виджет DPG имеющий размеры"""

    @final
    def setHeight(self, height: T) -> None:
        self._height = height

        if self.isRegistered():
            self._updateHeight()

    @final
    def getHeight(self) -> T:
        if self.isRegistered():
            self._width = dpg.get_item_height(self.tag())

        return self._height

    @final
    def _updateHeight(self):
        self.configure(height=self._height)
