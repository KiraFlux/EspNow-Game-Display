from abc import ABC
from dataclasses import dataclass
from typing import final

from dearpygui import dearpygui as dpg

from dpg_ui.abc.valued import Valued
from dpg_ui.core.dpg.item import DpgWidget


@dataclass
class DpgValuedWidget[T](DpgWidget, Valued[T], ABC):
    """Виджет со значением на стороне DPG"""

    @final
    def getValue(self) -> T:
        return dpg.get_value(self.tag())

    @final
    def setValue(self, value: T) -> None:
        dpg.set_value(self.tag(), value)
