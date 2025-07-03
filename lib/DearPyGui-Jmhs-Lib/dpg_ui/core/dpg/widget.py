from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from dataclasses import field
from typing import Optional
from typing import Self
from typing import final

from dearpygui import dearpygui as dpg

from dpg_ui.abc.font import Font
from dpg_ui.abc.widget import Widget
from dpg_ui.core.dpg.tag import DpgTag


@dataclass
class DpgWidget(Widget[DpgTag], ABC):
    """Виджет системы DPG"""

    __tag: Optional[DpgTag] = field(init=False, default=None)
    """Тег"""

    __font: Optional[Font] = field(init=False, default=None)
    """Шрифт"""

    def _onRegister(self, tag: DpgTag) -> None:
        if self.isRegistered():
            raise ValueError(f"re registering not allowed: {tag} (exist: {self.tag()}")

        self.__tag = tag

        if self.__font is not None:
            self.withFont(self.__font)

    @final
    def tag(self) -> Optional[DpgTag]:
        return self.__tag

    @final
    def configure(self, **kwargs) -> None:
        """Конфигурация виджета"""
        dpg.configure_item(self.tag(), **kwargs)

    @final
    def withFont(self, font: Font) -> Self:
        if self.isRegistered():
            dpg.bind_item_font(self.tag(), font.tag())
        else:
            self.__font = font

        return self

    @final
    def disable(self) -> None:
        dpg.disable_item(self.tag())

    @final
    def enable(self) -> None:
        dpg.enable_item(self.tag())

    @final
    def delete(self) -> None:
        dpg.delete_item(self.tag())

    @final
    def hide(self) -> None:
        dpg.hide_item(self.tag())

    @final
    def show(self) -> None:
        dpg.show_item(self.tag())
