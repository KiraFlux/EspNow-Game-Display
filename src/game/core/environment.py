from __future__ import annotations

import time
from typing import ClassVar
from typing import Final
from typing import Optional

from game.core.entities import Board
from game.core.entities import Mac
from game.core.entities import PlayerRegistry
from lina.vector import Vector2D
from misc.log import Logger


class Environment:
    """Сведения об игре"""

    _board_default_size: ClassVar = Vector2D(12, 8)
    _player_move_default_cooldown_secs: ClassVar = 5.0

    def __init__(self):
        self._log = Logger.inst().sub("env")

        self.host_mac: Optional[Mac] = None
        """Адрес узла хоста"""

        self.player_registry: Final = PlayerRegistry(self._log)
        """Реестр игроков"""

        self.board: Final = Board(self._board_default_size)
        """Игровое поле"""

        self.player_move_cooldown_secs = self._player_move_default_cooldown_secs
        """Тайм-аут отправки ходов"""

    def onPlayerMessage(self, mac: Mac, message: str) -> str:
        """Обработчик сообщения от игрока"""
        self._log.write(f"got player message from {mac} : '{message}'")

        player = self.player_registry.getPlayers().get(mac)

        if player is None:
            self.player_registry.register(mac, message)
            return f"{mac} Зарегистрирован как '{player}'"

        else:
            old_name = player.username

            player.rename(message)

            self._log.write(f"rename: {player}")
            return f"{mac} переименован: ({old_name} -> {player.username})"

    def onPlayerMove(self, mac: Mac, move: Vector2D[int]) -> str:
        """Обработчик хода игрока"""
        self._log.write(f"Получен ход от {mac}: '{move}'")

        player = self.player_registry.getPlayers().get(mac)

        if player is None:
            self._log.write(f"Ход {move} от {mac} отклонён (незарегистрированный клиент)")
            return f"Клиент {mac} (не зарегистрирован): Ход отклонён"

        now = time.time()

        time_since_last_move = now - player.last_send_secs

        if time_since_last_move < self.player_move_cooldown_secs:
            remaining_secs = self.player_move_cooldown_secs - time_since_last_move
            self._log.write(f"Ход {move} от {mac} отклонён (кулдаун: {remaining_secs:.1f} сек)")
            return f"{player}: Подождите ещё {remaining_secs:.1f} сек"

        player.last_send_secs = now

        result = self.board.makeMove(player, move)

        self._log.write(f"{mac} ход {move}: {result}")
        return f"{player}: Ход {move} выполнен: {result}"
