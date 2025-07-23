"""Модальное диалоговое окно"""
from abc import ABC
from abc import abstractmethod
from typing import Callable
from typing import Optional
from typing import final

from dpg_ui.abc.entities import Widget
from dpg_ui.abc.traits import Labeled
from dpg_ui.core.custom import CustomWidget
from dpg_ui.impl.buttons import Button
from dpg_ui.impl.containers import VBox
from dpg_ui.impl.containers import Window
from dpg_ui.impl.misc import Separator
from dpg_ui.impl.misc import Spacer
from dpg_ui.impl.text import Text
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


class ConfirmDialog(ModalDialog):
    """Диалог подтверждения"""

    def __init__(
            self,
            *,
            ok_button_label: str = "Ok"
    ):
        super().__init__()

        self._text = Text()
        self._button = Button()

        (
            self._window

            .add(
                VBox()

                .withWidth(400)

                .add(
                    self._text
                )

                .add(Separator())
                .add(
                    Spacer()
                    .withHeight(20)
                )

                .add(
                    self._button
                    .withLabel(ok_button_label)
                    .withWidth(-1)
                )
            )

        )

    def begin(
            self,
            text: str,
            *,
            on_confirm: Callable[[], None]
    ) -> None:
        """
        Запустить процедуру окна
        :param text:
        :param on_confirm:
        """

        def _f():
            on_confirm()
            self.hide()

        self._text.setValue(text)
        self._button.setHandler(_f)

        self.show()


class EditDialog[T](ModalDialog, ABC):
    """Модальный диалог редактирования"""

    @classmethod
    @abstractmethod
    def _getTitle(cls, value: T) -> str:
        """Получить заголовок из значения"""

    def __init__(self, content: Widget) -> None:
        super().__init__()

        self.__value: Optional[T] = None

        (
            self._window

            .add(content)

            .add(Separator())

            .add(Spacer().withHeight(30))

            .add(
                Button()
                .withLabel("Применить")
                .withWidth(-1)
                .withHandler(self._apply)
            )
        )

    def _apply(self) -> None:
        self.hide()

        if self.__value is not None:
            self.apply(self.__value)

    @abstractmethod
    def apply(self, value: T) -> None:
        """Применить изменения"""

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
