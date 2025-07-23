from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from enum import auto
from typing import Final
from typing import Mapping
from typing import Optional

from game.core.entities.player import Player
from game.core.entities.rules import ScoreRules
from rs.lina.vector import Vector2D
from rs.misc.subject import Subject


@dataclass(frozen=True)
class Cell:
    """Ячейка игрового поля"""

    owner: Player

    def isFriendly(self, other: Cell) -> bool:
        """Другая клетка является дружественной?"""
        return self.owner.team == other.owner.team

    def calcScore(self, rules: ScoreRules, other: Optional[Cell]) -> int:
        """Рассчитать счёт за соседнюю клетку"""

        if other is None:
            return rules.empty_cell

        if self.isFriendly(other):
            return rules.friend_cell
        else:
            return rules.enemy_cell


type Pos = Vector2D[int]


class Board:
    """Сведения об игровом поле"""

    def __init__(self, size: Pos, score_rules: ScoreRules) -> None:
        self._score_rules: Final = score_rules

        self._size = size
        self._state = dict[Pos, Cell]()

        self.size_subject: Final[Subject[Pos]] = Subject()
        self.move_subject: Final[Subject[tuple[Player, Pos]]] = Subject()
        self.update_subject: Final[Subject[Mapping[Pos, Cell]]] = Subject()

    @property
    def size(self) -> Pos:
        """Размер поля"""
        return self._size

    @size.setter
    def size(self, size: Pos) -> None:
        self._size = size
        self.size_subject.notify(self._size)

    def setSize(self, size: Pos) -> None:
        """setter версия"""
        self.size = size

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

    def reset(self) -> None:
        """Сбросить значения поля"""
        self._state.clear()
        self.update_subject.notify(self.getState())

    def makeMove(self, player: Player, pos: Pos) -> MakeMoveResult:
        """Совершить ход"""

        if not (0 <= pos.x < self.size.x) or not (0 <= pos.y < self.size.y):
            return Board.MakeMoveResult.OutOfBounds

        cell: Optional[Cell] = self._state.get(pos)

        if cell is not None:
            return Board.MakeMoveResult.CellNotEmpty

        self._state[pos] = cell = Cell(player)
        score = self._calcScore(cell, pos)

        player.score += score

        self.move_subject.notify((player, pos))
        return Board.MakeMoveResult.Ok

    def _calcScore(self, cell: Cell, pos: Pos) -> int:
        dy = Vector2D(0, 1)
        dx = Vector2D(1, 0)

        lookup = list()

        if self._score_rules.mode in ScoreRules.CellLookupMode.Orthogonal:
            lookup.extend((
                pos + dx,
                pos - dx,
                pos + dy,
                pos - dy,
            ))

        if self._score_rules.mode in ScoreRules.CellLookupMode.Diagonal:
            lookup.extend((
                pos + dx + dy,
                pos + dx - dy,
                pos - dx + dy,
                pos - dx - dy,
            ))

        return sum(
            cell.calcScore(self._score_rules, other)
            for other in map(self._state.get, lookup)
        )
