from typing import Final

from dpg_ui.core.custom import CustomWidget
from dpg_ui.impl.boxes import ColorInput
from dpg_ui.impl.boxes import IntDisplay
from dpg_ui.impl.boxes import IntInput
from dpg_ui.impl.boxes import TextInput
from dpg_ui.impl.buttons import Button
from dpg_ui.impl.containers import ChildWindow
from dpg_ui.impl.containers import Details
from dpg_ui.impl.containers import HBox
from dpg_ui.impl.containers import VBox
from dpg_ui.impl.text import Text
from game.core.entities.team import Team
from game.core.entities.team import TeamRegistry
from game.ui.dialog import EditDialog
from rs.misc.color import Color


class TeamEditDialog(EditDialog[Team]):
    """Диалог редактирования команды"""

    @classmethod
    def _getDefault(cls) -> Team:
        return Team.default()

    @classmethod
    def _getTitle(cls, team: Team) -> str:
        return team.__str__()

    def __init__(self) -> None:
        self._name: Final = TextInput()
        self._score: Final = IntInput(step=100, step_fast=1000)
        self._color = ColorInput(
            _value=Color.none(),
        )

        super().__init__(
            VBox()
            .add(
                self._name
                .withLabel("Название")
            )
            .add(
                self._score
                .withLabel("Общий счёт")
                .withInterval((0, 100000))
            )
            .add(
                self._color
            )
        )

    def apply(self, team: Team) -> None:
        super().apply(team)
        team.name = self._name.getValue()
        team.score = self._score.getValue()
        team.color = self._color.getValue()

    def begin(self, team: Team) -> None:
        super().begin(team)
        self._name.setValue(team.name)
        self._score.setValue(team.score)
        self._color.setValue(team.color)


class TeamCard(CustomWidget):
    """Карточка команды"""

    def __init__(self, team: Team, edit_button: Button):
        team.addObserver(self._update)

        self._name = Text(team.name, color=team.color)
        self._score = IntDisplay(default=team.score)

        base = (
            ChildWindow()
            .withHeight(70)
            .add(
                HBox()
                .add(
                    VBox()
                    .withWidth(50)
                    .add(self._score)
                    .add(edit_button)
                )
                .add(
                    HBox()
                    .withWidth(200)
                    .add(self._name)
                )
            )
        )

        super().__init__(base)

    def _update(self, team: Team) -> None:
        self._name.setValue(team.name)
        self._name.setColor(team.color)
        self._score.setValue(team.score)


class TeamList(CustomWidget):
    """Список команд"""

    def __init__(self, team_registry: TeamRegistry) -> None:
        self._team_list: Final = ChildWindow(scrollable_y=True)
        self._team_edit_dialog: Final = TeamEditDialog()

        for team in team_registry.teams():
            self._addTeamCard(team)

        team_registry.on_team_add.addObserver(self._addTeamCard)

        super().__init__(self._team_list)

    def _addTeamCard(self, team: Team) -> TeamCard:
        card = TeamCard(team, self._team_edit_dialog.createEditButton(team))
        self._team_list.add(card)
        return card
