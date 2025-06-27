from __future__ import annotations

from dataclasses import dataclass
from dataclasses import field
from typing import MutableSequence
from typing import Optional
from typing import Sequence


@dataclass
class Player:
    """Сведения об игроке"""

    username: str
    team: int
    last_send_ms: int


@dataclass
class GameInfo:
    """Сведения об игре"""

    host_mac: Optional[bytes] = None
    players: dict[bytes, Player] = field(init=False, default_factory=dict)
    field_state: dict[tuple[int, int], int] = field(init=False, default_factory=dict)
    logs: MutableSequence[str] = field(init=False, default_factory=list)

    def registerPlayer(self, username: str) -> Player:
        """Создать игрока"""
        return Player(
            username=username,
            team=len(self.players) + 1,
            last_send_ms=0
        )

    def onPlayerMessage(self, mac: bytes, message: str) -> str:
        """Обработчик сообщения от игрока"""
        mac_string = mac.hex('-', 2)

        player = self.players.get(mac)

        if player is None:
            player = self.players[mac] = self.registerPlayer(message)
            return f"Клиент {mac_string} (Игрок '{player.username}')"

        else:
            old_name = player.username
            player.username = message
            return f"Клиент {mac_string} переименован: ({old_name} -> {player.username})"

    def onPlayerMove(self, mac: bytes, move: tuple[int, int]) -> str:
        """Обработчик хода игрока"""
        mac_string = mac.hex('-', 2)

        player = self.players.get(mac)

        if player is None:
            return f"Клиент {mac_string} не зарегистрирован"

        return f"{mac_string} {player.username} Ход: ({move}) добавлен в очередь..."

    def log(self, message: str) -> None:
        """Записать лог"""
        self.logs.append(message)

    def getLogs(self) -> Sequence[str]:
        """Получить все логи и очистить"""
        ret = tuple(self.logs)
        self.logs.clear()
        return ret
