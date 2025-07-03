from __future__ import annotations

from typing import Mapping

from game.core.entities.mac import Mac
from misc.log import Logger
from misc.observer import Subject


class Player(Subject['Player']):
    """Сведения об игроке"""

    def __init__(self, mac: Mac, username: str, team: int) -> None:
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
    def team(self) -> int:
        """Номер команды"""
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
        return f"Игрок {self.mac} '{self.username}' (команда: {self.team})"


class PlayerRegistry(Subject[Player]):
    """Список игроков"""

    def __init__(self, log: Logger) -> None:
        super().__init__()
        self._log = log.sub("player-registry")
        self._players = dict[Mac, Player]()

    def register(self, mac: Mac, username: str) -> Player:
        """Зарегистрировать игрока"""

        p = Player(
            mac=mac,
            username=username,
            team=self._calcPlayerTeam(),
        )

        self._players[mac] = p
        self._log.write(f"registered: {p}")

        self.notifyObservers(p)

        return p

    def getPlayers(self) -> Mapping[Mac, Player]:
        """Получить игроков"""
        return self._players

    def _calcPlayerTeam(self):
        return len(self._players) + 1
