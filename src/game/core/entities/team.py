from typing import AbstractSet
from typing import Final

from game.impl.valuegen.color import ColorGenerator
from rs.misc.color import Color
from rs.misc.log import Logger
from rs.misc.observer import Subject


class Team(Subject['Team']):
    """Команда"""

    def __init__(self, name: str, color: Color) -> None:
        super().__init__()
        self._name = name
        self._color = color
        self._score: int = 0

    def __str__(self) -> str:
        return f"Команда '{self.name}'"

    @property
    def name(self) -> str:
        """Отображаемое имя команды"""
        return self._name

    @name.setter
    def name(self, n: str) -> None:
        self._name = n
        self.notifyObservers(self)

    @property
    def color(self) -> Color:
        """Цвет команды"""
        return self._color

    @color.setter
    def color(self, c: Color) -> None:
        self._color = c
        self.notifyObservers(self)

    @property
    def score(self) -> int:
        """Общий счёт команды"""
        return self._score

    @score.setter
    def score(self, s: int) -> None:
        self._score = s
        self.notifyObservers(self)


class TeamRegistry(Subject[Team]):
    """Реестр команд"""

    def __init__(self, color_generator: ColorGenerator) -> None:
        super().__init__()
        self._log = Logger("team-registry")
        self._team_index: int = 0

        self._color_generator: Final = color_generator
        self._teams: Final = set[Team]()

        self.default_team: Final = Team("default", Color.grey())

    def register(self, name: str) -> Team:
        """Зарегистрировать команду"""
        team = Team(name, self._color_generator.calc(self._calcTeamIndex()))

        self._teams.add(team)

        self.notifyObservers(team)
        self._log.write(f'registered: {team}')
        return team

    def unregister(self, team: Team) -> None:
        """Отменить регистрацию команды"""
        # self._teams.remove(team)

        self._log.write(f"unregistered: {team}")

    def teams(self) -> AbstractSet[Team]:
        """Получить существующие команды"""
        return self._teams

    def _calcTeamIndex(self) -> int:
        ret = self._team_index
        self._team_index += 1
        return ret
