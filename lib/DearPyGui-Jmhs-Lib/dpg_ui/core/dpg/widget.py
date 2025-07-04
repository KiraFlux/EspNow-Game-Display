from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from dataclasses import field
from typing import Optional
from typing import Self
from typing import final

from dearpygui import dearpygui as dpg

from dpg_ui.abc.entities import Font
from dpg_ui.abc.entities import Widget
from dpg_ui.core.dpg.item import DpgTag
from dpg_ui.core.dpg.traits import DpgDeletable
from dpg_ui.core.dpg.traits import DpgEnableable
from dpg_ui.core.dpg.traits import DpgVisibility


@dataclass
class DpgWidget(Widget[DpgTag], DpgDeletable, DpgEnableable, DpgVisibility, ABC):
    """Виджет системы DPG"""

    __font: Optional[Font] = field(init=False, default=None)
    """Шрифт"""

    def _onRegister(self, tag: DpgTag) -> None:
        super()._onRegister(tag)

        if self.__font is not None:
            self.withFont(self.__font)

    @final
    def withFont(self, font: Font[DpgTag]) -> Self:
        if self.isRegistered():
            dpg.bind_item_font(self.tag(), font.tag())

        else:
            self.__font = font

        return self

    @final
    def register(self, parent: Widget[DpgTag]) -> None:
        """Зарегистрировать виджет"""
        self._onRegister(self._createTag(parent.tag()))
