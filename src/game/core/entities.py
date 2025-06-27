from dataclasses import dataclass


@dataclass(frozen=True)
class Mac:
    """Обёртка над bytes MAC"""

    value: bytes

    def __post_init__(self):
        assert len(self.value) == 6

    def __str__(self) -> str:
        return self.value.hex('-', 1)


@dataclass(frozen=True)
class Vector2D[T]:
    """Ход игрока"""

    x: T
    y: T


@dataclass
class Player:
    """Сведения об игроке"""

    username: str
    team: int
    last_send_ms: int

    def __str__(self) -> str:
        return f"Игрок '{self.username}' (команда: {self.team})"
