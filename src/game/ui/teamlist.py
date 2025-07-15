from typing import Final

from dpg_ui.core.custom import CustomWidget
from dpg_ui.impl.boxes import ColorInput
from dpg_ui.impl.boxes import IntDisplay
from dpg_ui.impl.boxes import TextInput
from dpg_ui.impl.buttons import Button
from dpg_ui.impl.containers import ChildWindow
from dpg_ui.impl.containers import HBox
from dpg_ui.impl.containers import VBox
from dpg_ui.impl.text import Text
from game.core.entities.player import Team
from game.core.entities.player import TeamRegistry
from game.ui.dialog import EditDialog
from rs.misc.color import Color


class TeamEditDialog(EditDialog[Team]):
    """Диалог редактирования команды"""

    @classmethod
    def _getTitle(cls, team: Team) -> str:
        return team.__str__()

    def __init__(self) -> None:
        self._name: Final = TextInput()
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
                self._color
            )
        )

    def apply(self, team: Team) -> None:
        team.name = self._name.getValue()
        team.color = self._color.getValue()

    def begin(self, team: Team) -> None:
        super().begin(team)
        self._name.setValue(team.name)
        self._color.setValue(team.color)


class TeamCard(CustomWidget):
    """Карточка команды"""

    def __init__(self, team: Team, edit_button: Button):
        self._team: Final = team
        self._name_display = Text(team.name, color=team.color)
        self._score_display = IntDisplay(default=team.score)

        self._team.subject_change.addListener(self._update)

        base = (
            ChildWindow()
            .withHeight(100)
            .add(
                HBox()
                .add(
                    VBox()
                    .withWidth(50)
                    .add(self._score_display)
                    .add(edit_button)
                    .add(
                        Button()
                        .withLabel("X")
                        .withHandler(self.delete)
                    )
                )
                .add(
                    HBox()
                    .withWidth(200)
                    .add(self._name_display)
                )
            )
        )

        super().__init__(base)

    def _update(self, team: Team) -> None:
        self._name_display.setValue(team.name)
        self._name_display.setColor(team.color)
        self._score_display.setValue(team.score)

    def delete(self) -> None:
        self._team.subject_change.removeListener(self._update)
        super().delete()


class TeamList(CustomWidget):
    """Список команд"""

    def __init__(self, team_registry: TeamRegistry) -> None:
        self._team_registry: Final = team_registry
        self._team_list: Final = ChildWindow(scrollable_y=True)
        self._team_edit_dialog: Final = TeamEditDialog()

        for team in team_registry.getAll():
            self._addTeamCard(team)

        self._team_registry.on_team_add.addListener(self._addTeamCard)

        super().__init__(
            VBox()
            .add(
                Button()
                .withLabel("Добавить")
                .withWidth(-1)
                .withHandler(self._team_registry.register)
            )
            .add(self._team_list)
        )

    def _addTeamCard(self, team: Team) -> TeamCard:
        card = TeamCard(team, self._team_edit_dialog.createEditButton(team))
        card.attachDeleteObserver(lambda _: self._team_registry.unregister(team))

        self._team_list.add(card)
        return card
