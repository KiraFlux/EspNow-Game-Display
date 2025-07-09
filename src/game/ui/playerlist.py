from typing import Final

from dpg_ui.core.custom import CustomWidget
from dpg_ui.impl.boxes import IntDisplay
from dpg_ui.impl.boxes import IntInput
from dpg_ui.impl.boxes import TextInput
from dpg_ui.impl.buttons import Button
from dpg_ui.impl.containers import ChildWindow
from dpg_ui.impl.containers import ComboBox
from dpg_ui.impl.containers import HBox
from dpg_ui.impl.containers import VBox
from dpg_ui.impl.text import Text
from game.core.entities.player import Player
from game.core.entities.player import PlayerRegistry
from game.core.entities.team import Team
from game.core.entities.team import TeamRegistry
from game.ui.dialog import EditDialog
from rs.misc.color import Color
from rs.misc.log import Logger


class PlayerEditDialog(EditDialog[Player]):
    """Модальный диалог редактирования игрока"""

    def __init__(self, team_registry: TeamRegistry) -> None:
        self._username: Final = TextInput()
        self._score: Final = IntInput(step=10, step_fast=100)
        self._team: Final[ComboBox[Team]] = ComboBox()

        for t in team_registry.teams():
            self._team.add(t)

        team_registry.on_team_add.addObserver(self._team.add)

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
                .add(
                    self._team
                    .withLabel("Команда")
                )
            )
        )

    @classmethod
    def _getTitle(cls, value: Player) -> str:
        return value.username

    @classmethod
    def _getDefault(cls) -> Player:
        return Player.dummy()

    def apply(self, player: Player) -> None:
        super().apply(player)
        player.username = self._username.getValue()
        player.score = self._score.getValue()
        player.team = self._team.getValue()

    def begin(self, player: Player) -> None:
        super().begin(player)
        self._score.setValue(player.score)
        self._username.setValue(player.username)
        self._team.setValue(player.team)


class PlayerCard(CustomWidget):
    """Карточка игрока"""

    def __init__(self, player: Player, open_modal: Button):
        player.addObserver(self._update)

        self._mac = Text(f"MAC: {player.mac}", color=Color.grey())
        self._username = Text(player.username)
        self._team = Text(player.team.name, color=player.team.color)
        self._score = IntDisplay(default=player.score)

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

    def __init__(self, player_registry: PlayerRegistry, team_registry: TeamRegistry) -> None:
        self._log: Final = Logger('player-list')

        self._player_registry: Final = player_registry

        self._player_edit_dialog: Final = PlayerEditDialog(team_registry)
        self._player_list: Final = ChildWindow(scrollable_y=True)

        super().__init__(self._player_list)

        for p in self._player_registry.getPlayers().values():
            self._addPlayerCard(p)

        self._player_registry.on_player_add.addObserver(self._addPlayerCard)

    def _addPlayerCard(self, player: Player) -> None:
        card = PlayerCard(player, self._player_edit_dialog.createEditButton(player))
        card.attachDeleteObserver(lambda _: self._player_registry.unregister(player.mac))
        self._player_list.add(card)

        self._log.write(f"add {player}: {card}")
