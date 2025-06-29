from __future__ import annotations

import time
from typing import ClassVar
from typing import Final
from typing import Optional

from game.core.entities import Board
from game.core.entities import Mac
from game.core.entities import Player
from misc.log import Logger
from misc.vector import Vector2D


class Environment:
    """Сведения об игре"""

    _board_default_size: ClassVar = Vector2D(6, 6)
    _player_move_default_cooldown_secs: ClassVar = 10.0

    def __init__(self):
        self._log = Logger.inst().sub("env")

        self.host_mac: Optional[Mac] = None
        """Адрес узла хоста"""
        self.players: Final = dict[Mac, Player]()
        """Игроки"""
        self.board: Final = Board(self._board_default_size)
        """Игровое поле"""
        self.player_move_cooldown_secs = self._player_move_default_cooldown_secs
        """Тайм-аут отправки ходов"""

    def onPlayerMessage(self, mac: Mac, message: str) -> str:
        """Обработчик сообщения от игрока"""
        self._log.write(f"got player message from {mac} : '{message}'")

        player = self.players.get(mac)

        if player is None:
            player = self.players[mac] = self._registerPlayer(message)

            self._log.write(f"register: {player}")
            return f"{mac} Зарегистрирован как '{player}'"

        else:
            old_name = player.username
            player.username = message

            self._log.write(f"rename: {player}")
            return f"{mac} переименован: ({old_name} -> {player.username})"

    def onPlayerMove(self, mac: Mac, move: Vector2D[int]) -> str:
        """Обработчик хода игрока"""
        self._log.write(f"Получен ход от {mac}: '{move}'")

        player = self.players.get(mac)

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

    def _registerPlayer(self, username: str) -> Player:
        p = Player(username=username, team=self._calcPlayerTeam(), last_send_secs=0)

        self._log.write(f"registered: {p}")

        return p

    def _calcPlayerTeam(self):
        return len(self.players) + 1
