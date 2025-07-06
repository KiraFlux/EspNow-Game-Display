from typing import Optional

from dpg_ui.abc.entities import Font
from dpg_ui.abc.entities import Widget
from dpg_ui.abc.traits import Deletable
from dpg_ui.abc.traits import Visibility
from dpg_ui.core.dpg.item import DpgTag
from dpg_ui.core.dpg.widget import DpgWidget


class CustomWidget(Widget[DpgWidget], Deletable, Visibility):
    """Пользовательский виджет"""

    def __init__(self, base: DpgWidget) -> None:
        self.__base = base

    def isVisible(self) -> bool:
        return self.__base.isVisible()

    def setVisibility(self, is_visible: bool) -> None:
        self.__base.setVisibility(is_visible)

    def register(self, parent: Widget[DpgWidget]) -> None:
        self.__base.register(parent)

    def tag(self) -> Optional[DpgTag]:
        return self.__base.tag()

    def setFont(self, font: Font) -> None:
        self.__base.setFont(font)

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return self.__base._createTag(parent_tag)

    def delete(self) -> None:
        self.__base.delete()
