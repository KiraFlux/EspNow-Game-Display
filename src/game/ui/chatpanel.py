from typing import Final
from typing import Optional

from dpg_ui.core.custom import CustomWidget
from dpg_ui.impl.boxes import TextInput
from dpg_ui.impl.containers import ChildWindow
from dpg_ui.impl.containers import ComboBox
from dpg_ui.impl.containers import HBox
from dpg_ui.impl.containers import VBox
from dpg_ui.impl.misc import Separator
from dpg_ui.impl.misc import Spacer
from dpg_ui.impl.text import Text
from game.core.entities.player import Player
from game.core.environment import Environment
from game.res import Assets
from rs.misc.color import Color


class ChatPanel(CustomWidget):
    """Панель чата"""

    def __init__(self, env: Environment):
        player_select = ComboBox(
            _items_provider=lambda: env.player_registry.getAll().keys(),
            _value=None
        )

        def _f(_):
            player_select.update()

        env.player_registry.player_add_subject.addListener(_f)
        env.player_registry.player_remove_subject.addListener(_f)

        self._env: Final = env

        self._chat_current_player_text: Final = Text()
        self._chat_history_text: Final = Text()
        self._chats: Final = dict[Player, list[str]]()

        self._current_player: Optional[Player] = None

        super().__init__(
            VBox()
            .add(
                HBox()
                .withFont(Assets.title_font)
                .add(
                    Text("Попробуйте новый мессенджер ")
                )
                .add(
                    Text("XАМ", color=Color.nitro())
                )
            )

            .add(Separator())
            .add(Spacer().withHeight(50))

            .add(
                self._chat_current_player_text
                .withFont(Assets.label_font)
            )

            .add(
                ChildWindow(
                    scrollable_y=True,
                    resizable_y=True
                )
                .withHeight(400)
                .add(
                    self._chat_history_text
                    .withFont(Assets.log_font)
                )
            )

            .add(
                HBox()
                .add(
                    player_select
                    .withWidth(300)
                    .withHandler(lambda mac: self.setCurrentPlayer(env.player_registry.getAll()[mac]))
                )
                .add(
                    TextInput(
                        default="Сообщение от сервера",
                        on_enter=True
                    )
                    .withWidth(-1)
                    .withHandler(self._sendMessage)
                )
            )
        )

    def _sendMessage(self, message: str) -> None:
        if self._current_player is None:
            return

        self._env.protocol_message_sender(self._current_player.mac, message)

        messages = self._chats[self._current_player]
        messages.append(message)

        self._updateChatHistory(messages)

    def setCurrentPlayer(self, player: Player) -> None:
        self._current_player = player

        self._showChatWith(player)

    def _showChatWith(self, player: Player) -> None:
        self._chat_current_player_text.setValue(self._current_player.__str__())
        self._chat_current_player_text.setColor(self._current_player.team.color)

        messages = self._chats.get(player)

        if messages is None:
            messages = self._chats[player] = list()

        self._updateChatHistory(messages)

    def _updateChatHistory(self, messages):
        self._chat_history_text.setValue('\n'.join(messages))
