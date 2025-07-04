from dpg_ui.core.custom import CustomWidget
from dpg_ui.impl.checkbox import CheckBox
from dpg_ui.impl.containers import HBox
from dpg_ui.impl.containers import VBox
from dpg_ui.impl.containers import ChildWindow
from dpg_ui.impl.text import Text
from game.res import Assets
from misc.log import Logger


class LogView(CustomWidget):
    """Лог"""

    def __init__(self) -> None:
        self._text = Text().withFont(Assets.log_font)

        self._channels = VBox()

        self._active_channels = set[str]()

        base = (
            ChildWindow(
                background=True
            )
            .add(
                HBox()
                .add(
                    VBox()
                    .add(Text("Каналы").withFont(Assets.label_font))
                    .add(
                        ChildWindow(
                            width=300,
                            resizable_x=True,
                        )
                        .add(
                            self._channels
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

        Logger.on_write.addObserver(lambda _: self._onMessage())
        Logger.on_create.addObserver(self._createLogWidget)

        for key in Logger.getKeys():
            self._createLogWidget(key)

    def _createLogWidget(self, key: str) -> None:
        self._channels.add(
            CheckBox(
                key,
                _on_change=lambda state: self._onKeyWidget(key, state),
                _value_default=False,
            )
        )

    def _onKeyWidget(self, key: str, value: bool) -> None:
        if value:
            self._active_channels.add(key)

        else:
            self._active_channels.remove(key)

        self._onMessage()

    def _onMessage(self) -> None:
        self._text.setValue('\n'.join(Logger.getByFilter(tuple(self._active_channels))))
