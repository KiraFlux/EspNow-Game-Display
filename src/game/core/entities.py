from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from enum import StrEnum
from enum import auto
from typing import Mapping
from typing import MutableMapping

from misc.vector import Vector2D


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

    username: str
    team: int
    last_send_secs: float

    def __str__(self) -> str:
        return f"Игрок '{self.username}' (команда: {self.team})"


@dataclass(frozen=True)
class Cell:
    """Ячейка игрового поля"""

    owner: Player


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

        self._state[pos] = Cell(player)

        return Board.MakeMoveResult.Ok
