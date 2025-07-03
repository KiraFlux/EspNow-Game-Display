from abc import ABC
from dataclasses import dataclass
from typing import final

from dearpygui import dearpygui as dpg

from dpg_ui.abc.valued import Valued
from dpg_ui.core.dpg.widget import DpgWidget


@dataclass
class DpgValuedWidget[T](DpgWidget, Valued[T], ABC):
    """Виджет со значением на стороне DPG"""

    @final
    def getValue(self) -> T:
        if self.isRegistered():
            return dpg.get_value(self.tag())

        return self._value_default

    @final
    def setValue(self, value: T) -> None:
        if self.isRegistered():
            dpg.set_value(self.tag(), value)
        else:
            self._value_default = value
