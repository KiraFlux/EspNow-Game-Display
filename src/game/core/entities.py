from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from enum import StrEnum
from enum import auto
from typing import Mapping
from typing import MutableMapping
from typing import Optional

from lina.vector import Vector2D
from misc.log import Logger
from misc.observer import Subject


@dataclass(frozen=True)
class Mac:
    """Обёртка над bytes MAC"""

    value: bytes

    def __post_init__(self):
        assert len(self.value) == 6

    def __str__(self) -> str:
        return self.value.hex('-', 1)


@dataclass
class Player:
    """Сведения об игроке"""

    mac: Mac
    """MAC адрес"""
    username: str
    """Отображаемое имя"""
    team: int
    """Команда игрока"""
    score: int = 0
    """Счёт"""
    last_send_secs: float = 0
    """Время последней отправки"""

    def rename(self, new_username: str) -> None:
        """Переименовать игрока"""
        self.username = new_username

    def __str__(self) -> str:
        return f"Игрок '{self.username}' (команда: {self.team})"


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


@dataclass(frozen=True)
class Cell:
    """Ячейка игрового поля"""

    owner: Player

    def isFriendly(self, other: Cell) -> bool:
        """Другая клетка является дружественной?"""
        return self.owner.team == other.owner.team


@dataclass
class Board:
    """Сведения об игровом поле"""

    type Pos = Vector2D[int]

    size: Pos
    """Размеры поля"""
    _state: MutableMapping[Pos, Cell] = field(init=False, default_factory=dict)
    """Состояние поля"""

    def getState(self) -> Mapping[Pos, Cell]:
        """Получить состояние поля"""
        return self._state

    class MakeMoveResult(StrEnum):
        """Результат действия"""
        Ok = auto()
        """Успешный ход"""
        OutOfBounds = auto()
        """Ошибка: Ход за границей"""
        CellNotEmpty = auto()
        """Ошибка: Ход на занятую клетку"""

    def makeMove(self, player: Player, pos: Pos) -> MakeMoveResult:
        """Совершить ход"""

        if not (0 <= pos.x < self.size.x) or not (0 <= pos.y < self.size.y):
            return Board.MakeMoveResult.OutOfBounds

        cell: Optional[Cell] = self._state.get(pos)

        if cell is not None:
            return Board.MakeMoveResult.CellNotEmpty

        self._state[pos] = cell = Cell(player)
        player.score += self._calcScore(cell, pos)

        return Board.MakeMoveResult.Ok

    def _calcScore(self, cell: Cell, pos: Pos) -> int:
        dy = Vector2D.new(0, 1)
        dx = Vector2D.new(1, 0)

        up = self._state.get(pos + dy)
        down = self._state.get(pos - dy)
        left = self._state.get(pos + dx)
        right = self._state.get(pos + dx)

        neighbours = (up, down, left, right)

        if all(i is None for i in neighbours):
            return 0

        return sum(
            (1 if cell.isFriendly(i) else -1)
            for i in neighbours
            if i is not None
        )
