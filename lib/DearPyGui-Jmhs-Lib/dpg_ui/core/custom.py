from typing import Optional
from typing import Self

from dpg_ui.abc.entities import Font
from dpg_ui.abc.entities import Widget
from dpg_ui.abc.traits import Deletable
from dpg_ui.abc.traits import Enableable
from dpg_ui.abc.traits import Visibility
from dpg_ui.core.dpg.item import DpgTag
from dpg_ui.core.dpg.widget import DpgWidget


class CustomWidget(Deletable, Visibility, Enableable, Widget[DpgWidget]):
    """Пользовательский виджет"""

    def __init__(self, base: DpgWidget) -> None:
        self.__base = base

    def register(self, parent: Widget[DpgWidget]) -> None:
        self.__base.register(parent)

    def tag(self) -> Optional[DpgTag]:
        return self.__base.tag()

    def withFont(self, font: Font) -> Self:
        return self.__base.withFont(font)

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return self.__base._createTag(parent_tag)

    def show(self) -> None:
        self.__base.show()

    def hide(self) -> None:
        self.__base.hide()

    def enable(self) -> None:
        self.__base.enable()

    def disable(self) -> None:
        self.__base.disable()

    def delete(self) -> None:
        self.__base.delete()
