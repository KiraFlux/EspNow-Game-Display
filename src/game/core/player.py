from dataclasses import dataclass
from dataclasses import field
from typing import MutableSequence
from typing import Optional


@dataclass
class Player:
    """Сведения об игроке"""

    username: str
    team: int


@dataclass
class GameInfo:
    """Сведения об игре"""

    host_mac: Optional[bytes] = None
    players: dict[bytes, Player] = field(init=False, default_factory=dict)
    field_state: dict[tuple[int, int], int] = field(init=False, default_factory=dict)
    logs: MutableSequence[str] = field(init=False, default_factory=list)
