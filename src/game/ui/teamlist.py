from dpg_ui.core.custom import CustomWidget
from dpg_ui.impl.boxes import DisplayInt
from dpg_ui.impl.buttons import ColorDisplay
from dpg_ui.impl.containers import ChildWindow
from dpg_ui.impl.containers import HBox
from dpg_ui.impl.text import Text
from game.core.entities.team import Team
from game.core.entities.team import TeamRegistry


class TeamCard(CustomWidget):
    """Карточка команды"""

    def __init__(self, team: Team):
        team.addObserver(self._update)

        self._name = Text(team.name, color=team.color)
        self._score = DisplayInt("Счёт", default=team.score)
        self._color = ColorDisplay(_label='Цвет', _color=team.color)

        base = (
            ChildWindow(
                _height=100
            )
            .add(
                HBox()
                .add(self._color)
                .add(self._name)
            )
            .add(self._score)
        )

        super().__init__(base)

    def _update(self, team: Team) -> None:
        self._name.setValue(team.name)
        self._score.setValue(team.score)
        self._color.setColor(team.color)


class TeamList(CustomWidget):
    """Список команд"""

    def __init__(self, team_registry: TeamRegistry) -> None:
        team_list = ChildWindow()

        def _add_team_card(_team):
            team_list.add(TeamCard(_team))

        for team in team_registry.teams():
            _add_team_card(team)

        team_registry.addObserver(_add_team_card)

        super().__init__(team_list)
