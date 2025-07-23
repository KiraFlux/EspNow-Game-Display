from __future__ import annotations

from typing import AbstractSet
from typing import ClassVar
from typing import Final
from typing import Mapping
from typing import Optional

from game.core.entities.mac import Mac
from game.impl.valuegen.color import ColorGenerator
from rs.misc.color import Color
from rs.misc.log import Logger
from rs.misc.subject import Subject


class Player:
    """Сведения об игроке"""

    def __init__(self, mac: Mac, name: str) -> None:
        self.subject_change: Final[Subject[Player]] = Subject()

        self.mac: Final = mac
        self._name = name
        self.__current_team: Team = Team.default()

        self._score = 0
        self.last_send_secs = 0.0

    @property
    def name(self) -> str:
        """Имя пользователя"""
        return self._name

    @name.setter
    def name(self, new_username: str) -> None:
        self._name = new_username
        self.subject_change.notify(self)

    @property
    def team(self) -> Team:
        """Команда"""
        return self.__current_team

    def setTeam(self, new_team: Team):
        """Сменить команду"""

        if self.__current_team == new_team:
            return

        self.__current_team.removePlayer(self)
        new_team.addPlayer(self)

        self.__current_team = new_team
        self.subject_change.notify(self)

    @property
    def score(self) -> int:
        """Счёт игрока"""
        return self._score

    @score.setter
    def score(self, new_score: int) -> None:
        self._score = new_score
        self.subject_change.notify(self)

    def reset(self) -> None:
        """Сбросить значения игрока"""
        self.score = 0
        self.last_send_secs = 0.0

    def __str__(self) -> str:
        return f"Игрок {self.mac} '{self.name}'"


class PlayerRegistry:
    """Список игроков"""

    def __init__(self, team_registry: TeamRegistry) -> None:
        super().__init__()
        self._log = Logger("player-registry")

        self._team_registry: Final = team_registry
        self._players = dict[Mac, Player]()

        self.player_add_subject: Final[Subject[Player]] = Subject()
        self.player_remove_subject: Final[Subject[Player]] = Subject()

    def register(self, mac: Mac, username: str) -> Player:
        """Зарегистрировать игрока"""

        p = self._players[mac] = Player(mac, username)
        self.player_add_subject.notify(p)

        self._log.write(f"registered: {p}")
        return p

    def unregister(self, mac: Mac) -> None:
        """Удалить пользователя"""
        p = self._players.pop(mac)

        self.player_remove_subject.notify(p)

        self._log.write(f"unregistered: {p}")

    def getAll(self) -> Mapping[Mac, Player]:
        """Получить игроков"""
        return self._players


class Team:
    """Команда"""

    _default_instance: ClassVar[Optional[Team]] = None

    @classmethod
    def default(cls):
        """Команда по умолчанию"""
        if cls._default_instance is None:
            cls._default_instance = Team("default", Color.grey())

        return cls._default_instance

    def __init__(self, name: str, color: Color) -> None:
        self.subject_change: Final[Subject[Team]] = Subject()

        self._name = name
        self._color = color
        self._total_score: int = 0
        self._players: Final[set[Player]] = set()

    def __str__(self) -> str:
        return f"Команда '{self.name}'"

    @property
    def name(self) -> str:
        """Отображаемое имя команды"""
        return self._name

    @name.setter
    def name(self, n: str) -> None:
        self._name = n
        self.subject_change.notify(self)

    @property
    def color(self) -> Color:
        """Цвет команды"""
        return self._color

    @color.setter
    def color(self, c: Color) -> None:
        self._color = c
        self.subject_change.notify(self)

    @property
    def score(self) -> int:
        """Общий счёт команды"""
        return self._total_score

    def addPlayer(self, member: Player) -> None:
        """Добавить участника в команду"""
        if member in self._players:
            return

        self._players.add(member)
        member.subject_change.addListener(self._updateTotalScore)
        self._updateTotalScore()

    def removePlayer(self, player: Player) -> None:
        """Удалить участника из команды"""
        if player not in self._players:
            return

        self._players.remove(player)
        player.subject_change.removeListener(self._updateTotalScore)
        self._updateTotalScore()

    def _updateTotalScore(self, _=None) -> None:
        self._total_score = self._calcTotalScore()
        self.subject_change.notify(self)

    def _calcTotalScore(self) -> int:
        return sum(
            p.score
            for p in self._players
        )

    @property
    def players(self) -> AbstractSet[Player]:
        """Участники команды"""
        return self._players


class TeamRegistry:
    """Реестр команд"""

    def __init__(self, color_generator: ColorGenerator) -> None:
        self._color_generator: Final = color_generator

        self.__last_team_index: int = 0

        self._teams: Final = set[Team]()

        self.on_team_add: Final[Subject[Team]] = Subject()
        self.on_team_delete: Final[Subject[Team]] = Subject()
        self.on_team_update: Final[Subject[Team]] = Subject()

        # self._teams.add(Team.default())

        self._log: Final = Logger("team-registry")

    def register(self, name: str = None) -> Team:
        """Зарегистрировать команду"""

        team = Team(
            name or f"Команда {self.__last_team_index}",
            self._color_generator.calc(self.__last_team_index)
        )
        self.__last_team_index += 1

        self._teams.add(team)
        team.subject_change.addListener(self.on_team_update.notify)

        self.on_team_add.notify(team)
        self.on_team_update.notify(team)

        self._log.write(f'registered: {team}')
        return team

    def unregister(self, team: Team) -> None:
        """Отменить регистрацию команды"""
        if team is Team.default():
            return

        if team not in self._teams:
            return

        # Удаляем команду из реестра до перевода игроков
        team.subject_change.removeListener(self.on_team_update.notify)
        self._teams.remove(team)
        self.on_team_delete.notify(team)

        # Теперь безопасно переводим игроков
        default_team = Team.default()
        for player in tuple(team.players):
            player.setTeam(default_team)

        self._log.write(f"unregistered: {team}")

    def getAll(self) -> AbstractSet[Team]:
        """Получить существующие команды"""
        return self._teams
