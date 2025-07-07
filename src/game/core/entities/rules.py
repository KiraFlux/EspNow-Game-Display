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

    move_available: bool
    """Ходы разрешены"""

    def setMoveCooldown(self, cooldown_secs: float) -> None:
        """Установить кул-даун хода"""
        self.move_cooldown_secs = cooldown_secs

    def setMoveAvailable(self, available: bool) -> None:
        """Установить разрешение совершать ходы"""
        self.move_available = available
