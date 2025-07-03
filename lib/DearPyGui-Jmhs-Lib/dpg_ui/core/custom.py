from typing import Optional
from typing import Self

from dpg_ui.abc.font import Font
from dpg_ui.abc.widget import Widget


class CustomWidget[T](Widget):
    """Пользовательский виджет"""

    def __init__(self, base: Widget) -> None:
        self.__base = base

    def tag(self) -> Optional[T]:
        return self.__base.tag()

    def withFont(self, font: Font) -> Self:
        return self.__base.withFont(font)

    def show(self) -> None:
        self.__base.show()

    def register(self, parent: Widget) -> None:
        self.__base.register(parent)

    def hide(self) -> None:
        self.__base.hide()

    def enable(self) -> None:
        self.__base.enable()

    def disable(self) -> None:
        self.__base.disable()

    def delete(self) -> None:
        self.__base.delete()
