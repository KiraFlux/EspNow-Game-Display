from __future__ import annotations

from dataclasses import dataclass
from enum import IntFlag
from enum import auto
from typing import Iterable

from game.impl.valuegen.color import ColorGenerator


@dataclass(kw_only=True)
class ScoreRules:
    """Правила начисления счёта"""

    class CellLookupMode(IntFlag):
        """Режим просмотра клеток"""

        Diagonal = auto()
        Orthogonal = auto()
        Full = Diagonal | Orthogonal

        def __str__(self):
            return self.name

        @classmethod
        def getItems(cls) -> Iterable:
            return cls._member_map_.values()

    mode: CellLookupMode
    """Режим просмотра"""
    empty_cell: int
    """Очки за пустую клетку"""
    friend_cell: int
    """Дружественная клетка по прямой"""
    enemy_cell: int
    """Вражеская клетка по прямой"""

    def setCellLookupMode(self, v):
        self.mode = v

    def setEmptyCell(self, v):
        self.empty_cell = v

    def setFriendCell(self, v):
        self.friend_cell = v

    def setEnemyCell(self, v):
        self.enemy_cell = v


@dataclass(kw_only=True)
class GameRules:
    """Игровые правила"""

    score: ScoreRules
    """Правила начисления счёта"""

    team_color_generator: ColorGenerator
    """Генератор цвета команды"""

    move_cooldown_secs: float
    """Кул-даун ходов игрока"""

    move_available: bool
    """Ходы разрешены"""

    def setMoveCooldown(self, cooldown_secs: float) -> None:
        """Установить кул-даун хода"""
        self.move_cooldown_secs = cooldown_secs

    def setMoveAvailable(self, available: bool) -> None:
        """Установить разрешение совершать ходы"""
        self.move_available = available
