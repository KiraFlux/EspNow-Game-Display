from __future__ import annotations

from typing import Final
from typing import Mapping

from game.core.entities.mac import Mac
from game.core.entities.team import Team
from game.core.entities.team import TeamRegistry
from rs.misc.log import Logger
from rs.misc.observer import Subject


class Player(Subject['Player']):
    """Сведения об игроке"""

    @classmethod
    def dummy(cls):
        """Вернуть "Болванку" для значения по умолчанию"""
        return cls(
            mac=Mac.broadcast(),
            username="Dummy",
            team=Team.default(),
        )

    def __init__(self, mac: Mac, username: str, team: Team) -> None:
        super().__init__()
        self.mac = mac
        self._username = username
        self._team = team
        self._score = 0
        self.last_send_secs = 0.0

    @property
    def username(self) -> str:
        """Имя пользователя"""
        return self._username

    @username.setter
    def username(self, new_username: str) -> None:
        self._username = new_username
        self.notifyObservers(self)

    @property
    def team(self) -> Team:
        """Команда"""
        return self._team

    @team.setter
    def team(self, new_team: int) -> None:
        self._team = new_team
        self.notifyObservers(self)

    @property
    def score(self) -> int:
        """Счёт игрока"""
        return self._score

    @score.setter
    def score(self, new_score: int) -> None:
        self._score = new_score
        self.notifyObservers(self)

    def rename(self, new_username: str) -> None:
        """Переименовать игрока"""
        self.username = new_username

    def __str__(self) -> str:
        return f"Игрок {self.mac} '{self.username}' ({self.team})"


class PlayerRegistry:
    """Список игроков"""

    def __init__(self, team_registry: TeamRegistry) -> None:
        super().__init__()
        self._log = Logger("player-registry")

        self._team_registry: Final = team_registry
        self._players = dict[Mac, Player]()

        self.on_player_add: Final[Subject[Player]] = Subject()
        self.on_player_remove: Final[Subject[Player]] = Subject()

    def register(self, mac: Mac, username: str) -> Player:
        """Зарегистрировать игрока"""

        p = Player(
            mac=mac,
            username=username,
            team=Team.default(),
        )

        self._players[mac] = p
        self._log.write(f"registered: {p}")

        self.on_player_add.notifyObservers(p)

        return p

    def unregister(self, mac: Mac) -> None:
        """Удалить пользователя"""
        p = self._players.pop(mac)

        self.on_player_remove.notifyObservers(p)

        self._log.write(f"unregistered: {p}")

    def getPlayers(self) -> Mapping[Mac, Player]:
        """Получить игроков"""
        return self._players
