from dpg_ui.core.custom import CustomWidget
from dpg_ui.impl.boxes import DisplayInt
from dpg_ui.impl.containers import ChildWindow
from dpg_ui.impl.text import Text
from game.core.entities.team import Team
from game.core.entities.team import TeamRegistry


class TeamCard(CustomWidget):
    """Карточка команды"""

    def __init__(self, team: Team):
        team.addObserver(self._update)

        self.name = Text(team.name, color=team.color, bullet=True)
        self.score = DisplayInt("Счёт", team.score)

        base = (
            ChildWindow(
                _height=100
            )
            .add(self.name)
            .add(self.score)
        )

        super().__init__(base)

    def _update(self, team: Team) -> None:
        self.name.setValue(team.name)
        self.score.setValue(team.score)


class TeamList(CustomWidget):
    """Список команд"""

    def __init__(self, team_registry: TeamRegistry) -> None:
        team_list = (
            ChildWindow()
            .add(
                TeamCard(team_registry.default_team)
            )
        )

        team_registry.addObserver(
            lambda team: team_list.add(TeamCard(team))
        )

        super().__init__(team_list)
