from typing import Final

from kf_dpg.core.custom import CustomWidget
from kf_dpg.impl.boxes import ColorInput
from kf_dpg.impl.boxes import IntDisplay
from kf_dpg.impl.boxes import TextInput
from kf_dpg.impl.buttons import Button
from kf_dpg.impl.containers import ChildWindow
from kf_dpg.impl.containers import HBox
from kf_dpg.impl.containers import VBox
from kf_dpg.impl.text import Text
from game.core.entities.player import Team
from game.core.entities.player import TeamRegistry
from game.ui.dialog import ConfirmDialog
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

    def __init__(self, team: Team, edit_button: Button, delete_dialog: ConfirmDialog):
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
                        .withHandler(
                            lambda: delete_dialog.begin(
                                self._team.__str__(),
                                on_confirm=self.delete
                            )
                        )
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
        self._team_delete_dialog: Final = ConfirmDialog(ok_button_label="Отправить в испепелитесь").withLabel("Удалить команду?")

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
        card = TeamCard(team, self._team_edit_dialog.createEditButton(team), self._team_delete_dialog)
        card.attachDeleteObserver(lambda _: self._team_registry.unregister(team))

        self._team_list.add(card)
        return card
