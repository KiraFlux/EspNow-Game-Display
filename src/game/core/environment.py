from __future__ import annotations

import time
from typing import Final
from typing import Optional

from game.core.entities.board import Board
from game.core.entities.mac import Mac
from game.core.entities.player import PlayerRegistry
from game.core.entities.rules import GameRules
from lina.vector import Vector2D
from misc.log import Logger
from misc.observer import Subject


class Environment:
    """Сведения об игре"""

    def __init__(self, rules: GameRules):
        self._log = Logger("env")

        self.rules: Final = rules

        self._host_mac: Optional[Mac] = None
        self.host_mac_subject: Final[Subject[Mac]] = Subject()

        self.player_registry: Final = PlayerRegistry()

        self.board: Final = Board(Vector2D(12, 8), self.rules.score)

    @property
    def host_mac(self) -> Mac:
        """MAC адрес хоста"""
        return self._host_mac

    @host_mac.setter
    def host_mac(self, mac: Mac) -> None:
        self._host_mac = mac
        self.host_mac_subject.notifyObservers(self._host_mac)

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

        if time_since_last_move < self.rules.player_move_cooldown_secs:
            remaining_secs = self.rules.player_move_cooldown_secs - time_since_last_move
            self._log.write(f"Ход {move} от {mac} отклонён (кулдаун: {remaining_secs:.1f} сек)")
            return f"{player}: Подождите ещё {remaining_secs:.1f} сек"

        player.last_send_secs = now

        result = self.board.makeMove(player, move)

        self._log.write(f"{mac} ход {move}: {result}")
        return f"{player}: Ход {move} выполнен: {result}"
