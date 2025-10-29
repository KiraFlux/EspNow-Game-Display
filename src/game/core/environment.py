from __future__ import annotations

import time
from typing import Any
from typing import Callable
from typing import Final
from typing import Optional

from game.core.entities.board import Board
from game.core.entities.mac import Mac
from game.core.entities.player import PlayerRegistry
from game.core.entities.player import Team
from game.core.entities.player import TeamRegistry
from game.core.entities.rules import GameRules
from rs.lina.vector import Vector2D
from rs.misc.log import Logger
from rs.misc.subject import Subject


class Environment:
    """Сведения об игре"""

    def __init__(self, rules: GameRules):
        self._log = Logger("env")

        self.rules: Final = rules

        self._host_mac: Optional[Mac] = None
        self.host_mac_subject: Final[Subject[Mac]] = Subject()

        self.team_registry: Final = TeamRegistry(self.rules.team_color_generator, self.rules.team_name_generator)
        self.player_registry: Final = PlayerRegistry(self.team_registry)

        self.board: Final = Board(Vector2D(Board.max_size, Board.max_size), self.rules.score)

        self.protocol_message_sender: Callable[[Mac, str], Any] = self._mockMessageSender

    def _mockMessageSender(self, mac: Mac, message: str) -> None:
        self._log.write(f"MOCK: Отправка {mac} : '{message}'")

    @property
    def host_mac(self) -> Mac:
        """MAC адрес хоста"""
        return self._host_mac

    @host_mac.setter
    def host_mac(self, mac: Mac) -> None:
        self._host_mac = mac
        self.host_mac_subject.notify(self._host_mac)

    def onPlayerMessage(self, mac: Mac, message: str) -> str:
        """Обработчик сообщения от игрока"""
        self._log.write(f"got player message from {mac} : '{message}'")

        player = self.player_registry.getAll().get(mac)

        if player is None:
            self.player_registry.register(mac, message)
            return f"{mac} Зарегистрирован как '{player}'"

        else:
            old_name = player.name
            player.name = message

            self._log.write(f"rename: {player}")
            return f"{mac} переименован: ({old_name} -> {player.name})"

    def onPlayerMove(self, mac: Mac, move: Vector2D[int]) -> str:
        """Обработчик хода игрока"""
        self._log.write(f"Получен ход от {mac}: '{move}'")

        if not self.rules.move_available:
            s = "Ход от игроков ещё не разрешены"
            self._log.write(s)
            return s

        player = self.player_registry.getAll().get(mac)

        if player is None:
            s = f"Клиент {mac} (не зарегистрирован): Ход отклонён"
            self._log.write(s)
            return s

        if player.team == Team.default():
            s = f"{player}: Вы не можете совершать ход не имея принадлежности к команде"
            self._log.write(s)
            return s

        now = time.time()

        time_since_last_move = now - player.last_send_secs

        if time_since_last_move < self.rules.move_cooldown_secs:
            remaining_secs = self.rules.move_cooldown_secs - time_since_last_move
            s = f"{player}: Подождите ещё {remaining_secs:.1f} сек"
            self._log.write(s)
            return s

        player.last_send_secs = now

        result = self.board.makeMove(player, move)

        s = f"{player}: Ход {move} выполнен: {result}"
        self._log.write(s)
        return s
