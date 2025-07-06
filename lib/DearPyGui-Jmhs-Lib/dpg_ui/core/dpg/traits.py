from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import Callable
from typing import Optional
from typing import final

from dearpygui import dearpygui as dpg

from dpg_ui.abc.traits import CallbackSupport
from dpg_ui.abc.traits import Colored
from dpg_ui.abc.traits import Deletable
from dpg_ui.abc.traits import Intervaled
from dpg_ui.abc.traits import Labelable
from dpg_ui.abc.traits import Sizable
from dpg_ui.abc.traits import Toggleable
from dpg_ui.abc.traits import Valued
from dpg_ui.abc.traits import Visibility
from dpg_ui.abc.traits import WidthAdjustable
from dpg_ui.core.dpg.item import DpgItem
from rs.color import Color


class DpgLabelable(DpgItem, Labelable):
    """Объект Dpg имеющий метку (label)"""

    @final
    def getLabel(self) -> Optional[str]:
        if self.isRegistered():
            self._label = dpg.get_item_label(self.tag())

        return self._label

    @final
    def setLabel(self, label: Optional[str]) -> None:
        self._label = label

        if self.isRegistered():
            self._updateLabel()

    def _updateLabel(self) -> None:
        dpg.set_item_label(self.tag(), self._label)

    def update(self) -> None:
        super().update()
        self._updateLabel()


class DpgColored(DpgItem, Colored):
    @final
    def setColor(self, color: Color) -> None:
        self._color = color

        if self.isRegistered():
            self._updateColor()

    def _updateColor(self):
        self.configure(color=super().getColor().toRGBA8888())

    def update(self) -> None:
        super().update()
        self._updateColor()


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

    def _updateEnabled(self) -> None:
        if self._enabled:
            dpg.enable_item(self.tag())
        else:
            dpg.disable_item(self.tag())

    def update(self) -> None:
        super().update()
        self._updateEnabled()


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

    def _updateVisibility(self) -> None:
        if self._visible:
            dpg.show_item(self.tag())
        else:
            dpg.hide_item(self.tag())

    def update(self) -> None:
        super().update()
        self._updateVisibility()


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

    def _updateValue(self):
        dpg.set_value(self.tag(), self._value)

    def update(self) -> None:
        super().update()
        self._updateValue()


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

    def _updateIntervalMax(self) -> None:
        self.configure(max_value=self._interval_max)

    def _updateIntervalMin(self) -> None:
        self.configure(min_value=self._interval_min)

    def update(self) -> None:
        super().update()
        self._updateIntervalMin()
        self._updateIntervalMax()


class _DpgCallbackSupport[F: Callable](DpgItem, CallbackSupport[F], ABC):

    @abstractmethod
    def _createCallbackWrapper(self) -> Callable[[Any], Any]:
        """Создать обёртку для передачи в DPG"""

    @final
    def setCallback(self, f: F) -> None:
        self._callback = f

        if self.isRegistered():
            self._updateCallback()

    def _updateCallback(self) -> None:
        self.configure(
            callback=(
                None
                if self._callback is None else
                self._createCallbackWrapper()
            )
        )

    def update(self) -> None:
        super().update()
        self._updateCallback()


class DpgValuedCallbackSupport[T](DpgValued[T], _DpgCallbackSupport[Callable[[T], Any]]):
    """Объект DPG поддерживающий обратный вызов со значением"""

    def _createCallbackWrapper(self) -> Callable[[Any], Any]:
        return lambda _: self._callback(self.getValue())


class DpgCallbackSupport(_DpgCallbackSupport[Callable[[], Any]]):
    """Объект DPG поддерживающий обратный вызов"""

    def _createCallbackWrapper(self) -> Callable[[Any], Any]:
        return lambda _: self._callback()


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

    def _updateWidth(self) -> None:
        self.configure(width=self._width)

    def update(self) -> None:
        super().update()
        self._updateWidth()


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

    def _updateHeight(self):
        self.configure(height=self._height)

    def update(self) -> None:
        super().update()
        self._updateHeight()
