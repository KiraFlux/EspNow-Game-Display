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

    __tag: Optional[DpgTag] = field(init=False, default=None)
    """Тег"""

    def _onRegister(self, tag: DpgTag) -> None:
        if self.__tag is not None:
            raise ValueError(f"re registering not allowed: {tag} (exist: {self.tag()}")

        self.__tag = tag

    @final
    def tag(self) -> DpgTag:
        return self.__tag

    @final
    def configure(self, **kwargs) -> None:
        """Конфигурация виджета"""
        dpg.configure_item(self.tag(), **kwargs)
