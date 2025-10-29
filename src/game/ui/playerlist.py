from typing import Final

from kf_dpg.core.custom import CustomWidget
from kf_dpg.impl.boxes import IntDisplay
from kf_dpg.impl.boxes import IntInput
from kf_dpg.impl.boxes import TextInput
from kf_dpg.impl.buttons import Button
from kf_dpg.impl.containers import ChildWindow
from kf_dpg.impl.containers import ComboBox
from kf_dpg.impl.containers import HBox
from kf_dpg.impl.containers import VBox
from kf_dpg.impl.text import Text
from game.core.entities.player import Player
from game.core.entities.player import PlayerRegistry
from game.core.entities.player import Team
from game.core.entities.player import TeamRegistry
from game.ui.dialog import ConfirmDialog
from game.ui.dialog import EditDialog
from rs.misc.color import Color
from rs.misc.log import Logger


class PlayerEditDialog(EditDialog[Player]):
    """Модальный диалог редактирования игрока"""

    def __init__(self, team_registry: TeamRegistry) -> None:
        self._name_input: Final = TextInput()
        self._score_input: Final = IntInput(step=10, step_fast=100)

        self._team_combo: Final[ComboBox[Team]] = ComboBox(
            _value=None,
            _items_provider=team_registry.getAll
        )

        team_registry.on_team_add.addListener(self._updateTeamList)
        team_registry.on_team_update.addListener(self._updateTeamList)
        team_registry.on_team_delete.addListener(self._updateTeamList)

        super().__init__(
            (
                VBox()
                .add(
                    self._name_input
                    .withLabel("Username")
                )
                .add(
                    self._score_input
                    .withLabel("Счёт")
                    .withInterval((0, 10000))
                )
                .add(
                    self._team_combo
                    .withLabel("Команда")
                )
            )
        )

    @classmethod
    def _getTitle(cls, value: Player) -> str:
        return value.name

    def apply(self, player: Player) -> None:
        player.name = self._name_input.getValue()
        player.score = self._score_input.getValue()
        t = self._team_combo.getValue()
        player.setTeam(t)

    def begin(self, player: Player) -> None:
        super().begin(player)
        self._score_input.setValue(player.score)
        self._name_input.setValue(player.name)
        self._team_combo.setValue(player.team)

    def _updateTeamList(self, _=None) -> None:
        self._team_combo.update()


class PlayerCard(CustomWidget):
    """Карточка игрока"""

    def __init__(self, player: Player, open_modal: Button, delete_dialog: ConfirmDialog):
        self._target_player: Final = player
        self._current_team = player.team

        self._mac_display = Text(f"MAC: {player.mac}", color=Color.grey())
        self._name_display = Text(player.name)
        self._score_display = IntDisplay(default=player.score)
        self._team_name_display = Text(self._current_team.name, color=self._current_team.color)

        player.subject_change.addListener(self._updatePlayer)
        self._current_team.subject_change.addListener(self._updateTeam)

        super().__init__(
            ChildWindow()
            .withHeight(100)
            .add(
                HBox()
                .add(
                    VBox()
                    .withWidth(50)
                    .add(self._score_display)
                    .add(
                        open_modal
                    )
                    .add(
                        Button()
                        .withLabel("X")
                        .withHandler(
                            lambda: delete_dialog.begin(
                                self._target_player.__str__(),
                                on_confirm=self.delete
                            )
                        )
                    )
                )
                .add(
                    VBox()
                    .add(self._mac_display)
                    .add(self._name_display)
                    .add(self._team_name_display)
                )
            )
        )

    def _updatePlayer(self, player: Player) -> None:
        self._name_display.setValue(player.name)
        self._score_display.setValue(player.score)

        if player.team != self._current_team:
            self._current_team.subject_change.removeListener(self._updateTeam)
            self._current_team = player.team
            self._current_team.subject_change.addListener(self._updateTeam)

            self._updateTeam(self._current_team)

    def _updateTeam(self, team: Team) -> None:
        self._team_name_display.setValue(team.name)
        self._team_name_display.setColor(team.color)

    def delete(self) -> None:
        self._current_team.subject_change.removeListener(self._updateTeam)
        self._target_player.subject_change.removeListener(self._updatePlayer)
        super().delete()


class PlayerList(CustomWidget):
    """Список игроков"""

    def __init__(self, player_registry: PlayerRegistry, team_registry: TeamRegistry) -> None:
        self._log: Final = Logger('player-list')

        self._player_registry: Final = player_registry

        self._player_edit_dialog: Final = PlayerEditDialog(team_registry)
        self._player_delete_dialog: Final = ConfirmDialog(ok_button_label="Скатертью дорожка!").withLabel("Отправить погулять?")
        self._player_list: Final = ChildWindow(scrollable_y=True)

        super().__init__(self._player_list)

        for p in self._player_registry.getAll().values():
            self._addPlayerCard(p)

        self._player_registry.player_add_subject.addListener(self._addPlayerCard)

    def _addPlayerCard(self, player: Player) -> None:
        card = PlayerCard(player, self._player_edit_dialog.createEditButton(player), self._player_delete_dialog)
        card.attachDeleteObserver(lambda _: self._player_registry.unregister(player.mac))
        self._player_list.add(card)

        self._log.write(f"add {player}")
