from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from dataclasses import field
from typing import Optional
from typing import final

from dearpygui import dearpygui as dpg

from dpg_ui.abc.widget import Widget

DpgTag = int | str


@dataclass
class DpgWidget(Widget[DpgTag], ABC):
    """Виджет системы DPG"""

    _tag: Optional[DpgTag] = field(init=False, default=None)
    """Тег"""

    @final
    def tag(self) -> DpgTag:
        return self._tag

    @final
    def configure(self, **kwargs) -> None:
        """Конфигурация виджета"""
        dpg.configure_item(self.tag(), **kwargs)
