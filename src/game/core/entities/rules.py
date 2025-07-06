from dataclasses import dataclass

from game.impl.valuegen.color import ColorGenerator


@dataclass(kw_only=True)
class ScoreRules:
    """Правила начисления счёта"""

    friend_cell: int
    """Дружественная клетка по прямой"""
    enemy_cell: int
    """Вражеская клетка по прямой"""


@dataclass(kw_only=True)
class GameRules:
    """Игровые правила"""

    score: ScoreRules
    """Правила начисления счёта"""

    team_color_generator: ColorGenerator
    """Генератор цвета команды"""

    move_cooldown_secs: float
    """Кул-даун ходов игрока"""

    moves_available: bool
    """Ходы разрешены"""
