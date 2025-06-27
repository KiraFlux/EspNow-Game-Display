from __future__ import annotations

from typing import Final
from typing import Optional

from game.core.entities import Mac
from game.core.entities import Player
from game.core.entities import Vector2D
from game.core.log import Logger


class Environment:
    """Сведения об игре"""

    def __init__(self):
        self.log = Logger.inst().sub("env")

        self.host_mac: Optional[Mac] = None
        """Адрес узла хоста"""

        self.players: Final = dict[Mac, Player]()
        """Игроки"""

        self.board_state: Final = dict[Vector2D[int], Player]()
        """Состояние доски (позиция ячейки - команда)"""
        self.board_size: Vector2D[int]
        """Размер доски"""

    def registerPlayer(self, username: str) -> Player:
        """Создать игрока"""
        p = Player(username=username, team=self._calcPlayerTeam(), last_send_ms=0)
        self.log.write(f"registered: {p}")
        return p

    def onPlayerMessage(self, mac: Mac, message: str) -> str:
        """Обработчик сообщения от игрока"""

        player = self.players.get(mac)

        if player is None:
            player = self.players[mac] = self.registerPlayer(message)
            return f"{mac} Зарегистрирован как '{player}'"

        else:
            old_name = player.username
            player.username = message
            return f"{mac} переименован: ({old_name} -> {player.username})"

    def onPlayerMove(self, mac: Mac, move: Vector2D[int]) -> str:
        """Обработчик хода игрока"""

        player = self.players.get(mac)

        if player is None:
            return f"Клиент {mac} (не зарегистрирован) : Ход отклонён"

        return f"{player.username} Ход: {move} добавлен в очередь..."

    def _calcPlayerTeam(self):
        return len(self.players) + 1
