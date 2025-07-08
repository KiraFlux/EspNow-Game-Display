from typing import Final

from dpg_ui.core.custom import CustomWidget
from dpg_ui.impl.boxes import DisplayInt
from dpg_ui.impl.boxes import InputInt
from dpg_ui.impl.boxes import InputText
from dpg_ui.impl.buttons import Button
from dpg_ui.impl.containers import ChildWindow
from dpg_ui.impl.containers import HBox
from dpg_ui.impl.containers import VBox
from dpg_ui.impl.text import Text
from game.core.entities.player import Player
from game.core.entities.player import PlayerRegistry
from game.ui.dialog import EditDialog
from rs.misc.color import Color


class PlayerEditDialog(EditDialog[Player]):
    """Модальный диалог редактирования игрока"""

    def __init__(self) -> None:
        self._username: Final = InputText()
        self._score: Final = InputInt(step=10, step_fast=100)
        super().__init__(
            (
                VBox()
                .add(
                    self._username
                    .withLabel("Username")
                )
                .add(
                    self._score
                    .withLabel("Счёт")
                    .withInterval((0, 10000))
                )
            )
        )

    @classmethod
    def _getTitle(cls, value: Player) -> str:
        return value.username

    @classmethod
    def _getDefault(cls) -> Player:
        return Player.dummy()

    def apply(self, value: Player) -> None:
        super().apply(value)
        value.username = self._username.getValue()
        value.score = self._score.getValue()

    def begin(self, player: Player) -> None:
        super().begin(player)
        self._score.setValue(player.score)
        self._username.setValue(player.username)


class PlayerCard(CustomWidget):
    """Карточка игрока"""

    def __init__(self, player: Player, open_modal: Button):
        player.addObserver(self._update)

        self._mac = Text(f"MAC: {player.mac}", color=Color.grey())
        self._username = Text(player.username)
        self._team = Text(player.team.name, color=player.team.color)
        self._score = DisplayInt(default=player.score)

        super().__init__(
            ChildWindow()
            .withHeight(100)
            .add(
                HBox()
                .add(
                    VBox()
                    .withWidth(50)
                    .add(self._score)
                    .add(
                        open_modal
                    )
                    .add(
                        Button()
                        .withLabel("X")
                        .withHandler(self.delete)
                    )
                )
                .add(
                    VBox()
                    .add(self._mac)
                    .add(self._username)
                    .add(self._team)
                )
            )
        )

    def _update(self, p: Player) -> None:
        self._username.setValue(p.username)
        self._team.setValue(p.team.name)
        self._team.setColor(p.team.color)
        self._score.setValue(p.score)


class PlayerList(CustomWidget):
    """Список игроков"""

    def __init__(self, player_registry: PlayerRegistry) -> None:
        self._player_registry: Final = player_registry
        self._player_registry.addObserver(self._addPlayerCard)

        self._player_edit_dialog: Final = PlayerEditDialog()
        self._player_list: Final = ChildWindow(scrollable_y=True)

        super().__init__(self._player_list)

        for player in self._player_registry.getPlayers().values():
            self._addPlayerCard(player)

    def _addPlayerCard(self, player: Player) -> None:
        card = PlayerCard(player, self._player_edit_dialog.createEditButton(player))
        card.attachDeleteObserver(lambda _: self._player_registry.unregister(player.mac))
        self._player_list.add(card)
