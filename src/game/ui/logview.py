from kf_dpg.core.custom import CustomWidget
from kf_dpg.impl.buttons import CheckBox
from kf_dpg.impl.containers import ChildWindow
from kf_dpg.impl.containers import HBox
from kf_dpg.impl.containers import VBox
from kf_dpg.impl.text import Text
from game.assets import Assets
from rs.misc.log import Logger


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
                    .add(
                        Text("Каналы")
                        .withFont(Assets.title_font)
                    )
                    .add(
                        ChildWindow(
                            _width=300,
                            resizable_x=True,
                            scrollable_y=True
                        )
                        .add(
                            self._channels
                        )
                    )
                )
                .add(
                    ChildWindow(
                        scrollable_y=True
                    )
                    .add(self._text)
                )
            )
        )

        super().__init__(base)

        Logger.on_write.addListener(lambda _: self._onMessage())
        Logger.on_create.addListener(self._createLogWidget)

        for key in Logger.getKeys():
            self._createLogWidget(key)

    def _createLogWidget(self, key: str) -> None:
        self._channels.add(
            CheckBox(
                _value=False,
            )
            .withLabel(key)
            .withHandler(
                lambda state: self._onKeyWidget(key, state)
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
