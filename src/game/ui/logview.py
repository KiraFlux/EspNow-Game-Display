from dpg_ui.core.custom import CustomWidget
from dpg_ui.impl.checkbox import CheckBox
from dpg_ui.impl.container.box import HBox
from dpg_ui.impl.container.box import VBox
from dpg_ui.impl.container.window import ChildWindow
from dpg_ui.impl.text import Text
from game.res import Assets
from misc.log import Logger


class LogView(CustomWidget):
    """Лог"""

    def __init__(self) -> None:
        self._text = Text().withFont(Assets.log_font)

        self._filters_container = VBox()

        self._active_filters = set[str]()

        base = (
            ChildWindow(
                background=True
            )
            .add(
                HBox()
                .add(
                    VBox()
                    .add(Text("Фильтры").withFont(Assets.label_font))
                    .add(
                        ChildWindow(
                            width=300,
                            resizable_x=True,
                        )
                        .add(
                            self._filters_container
                        )
                    )
                )
                .add(
                    ChildWindow()
                    .add(self._text)
                )
            )
        )

        super().__init__(base)

        Logger.on_write = self._onMessage
        Logger.on_create = self._createLogWidget

        for key in Logger.getKeys():
            self._createLogWidget(key)

    def _createLogWidget(self, key: str) -> None:
        self._filters_container.add(
            CheckBox(
                key,
                on_change=lambda state: self._onKeyWidget(key, state),
                _value_default=False,
            )
        )

    def _onKeyWidget(self, key: str, value: bool) -> None:
        if value:
            self._active_filters.add(key)

        else:
            self._active_filters.remove(key)

        self._onMessage()

    def _onMessage(self) -> None:
        self._text.setValue('\n'.join(Logger.getByFilter(tuple(self._active_filters))))
