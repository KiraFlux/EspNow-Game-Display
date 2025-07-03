from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from enum import auto
from typing import Mapping
from typing import Optional

from game.core.entities.player import Player
from lina.vector import Vector2D
from misc.observer import Subject


@dataclass(frozen=True)
class Cell:
    """Ячейка игрового поля"""

    owner: Player

    def isFriendly(self, other: Cell) -> bool:
        """Другая клетка является дружественной?"""
        return self.owner.team == other.owner.team


type Pos = Vector2D[int]


class Board:
    """Сведения об игровом поле"""

    def __init__(self, size: Pos) -> None:
        self._size = size
        self._state = dict[Pos, Cell]()
        self.size_subject: Subject[Pos] = Subject()
        self.move_subject: Subject[tuple[Player, Pos]] = Subject()

    @property
    def size(self) -> Pos:
        """Размер поля"""
        return self._size

    @size.setter
    def size(self, new_size: Pos) -> None:
        self._size = new_size
        self.size_subject.notifyObservers(self._size)

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

        self.move_subject.notifyObservers((player, pos))
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
