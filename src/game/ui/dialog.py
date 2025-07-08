"""Модальное диалоговое окно"""
from abc import ABC
from abc import abstractmethod
from typing import Optional
from typing import final

from dpg_ui.abc.traits import Deletable
from dpg_ui.abc.traits import Labeled
from dpg_ui.core.custom import CustomWidget
from dpg_ui.impl.buttons import Button
from dpg_ui.impl.containers import HBox
from dpg_ui.impl.containers import Window
from dpg_ui.impl.misc import Separator
from dpg_ui.impl.misc import Spacer
from game.res import Assets


class ModalDialog(CustomWidget, Labeled):
    """Модальный диалог"""

    def __init__(self):
        self._window = Window(
            _auto_size=True,
            _modal=True,
        ).withFont(Assets.default_font)

        super().__init__(self._window)

    def getLabel(self) -> Optional[str]:
        return self._window.getLabel()

    def setLabel(self, label: Optional[str]) -> None:
        self._window.setLabel(label)


class EditDialog[T](ModalDialog, ABC):
    """Модальный диалог редактирования"""

    @classmethod
    @abstractmethod
    def _getDefault(cls) -> T:
        """Значение по умолчанию"""

    @classmethod
    @abstractmethod
    def _getTitle(cls, value: T) -> str:
        """Получить заголовок из значения"""

    def __init__(self, content: Deletable) -> None:
        super().__init__()

        self.__value: T = self._getDefault()

        (
            self._window

            .add(content)

            .add(Separator())

            .add(Spacer().withHeight(30))

            .add(
                HBox()
                .withWidth(300)
                .add(
                    Button()
                    .withLabel("Применить")
                    .withHandler(lambda: self.apply(self.__value))
                )
                .add(
                    Button()
                    .withLabel("Отмена")
                    .withHandler(self.hide)
                )
            )
        )

    def apply(self, value: T) -> None:
        """Применить изменения"""
        self.hide()

    def begin(self, value: T) -> None:
        """Перенастроить диалог к редактированию этого игрока"""
        self.show()
        self.__value = value
        self._window.setLabel(f"Редактирование: {self._getTitle(value)}")

    @final
    def createEditButton(self, value: T) -> Button:
        """Создать кнопку для открытия диалога редактирования данного игрока"""
        return (
            Button()
            .withLabel("···")
            .withHandler(lambda: self.begin(value))
        )
