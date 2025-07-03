from __future__ import annotations

import time
from typing import ClassVar
from typing import Final
from typing import Optional

from game.core.entities.board import Board
from game.core.entities.mac import Mac
from game.core.entities.player import PlayerRegistry
from game.impl.valuegen.color import ColorGenerator
from game.impl.valuegen.loopstep import LoopStepGenerator
from game.impl.valuegen.phasedamplitude import PhasedAmplitudeGenerator
from lina.vector import Vector2D
from misc.log import Logger


class Environment:
    """Сведения об игре"""

    _board_default_size: ClassVar = Vector2D(12, 8)
    _player_move_default_cooldown_secs: ClassVar = 5.0

    def __init__(self):
        self._log = Logger.inst().sub("env")

        self.host_mac: Optional[Mac] = None

        self.player_registry: Final = PlayerRegistry(self._log)

        self.board: Final = Board(self._board_default_size)

        self.player_move_cooldown_secs = self._player_move_default_cooldown_secs

        self.team_color_generator: Final = ColorGenerator(
            hue=LoopStepGenerator(
                start=15,
                step=200,
                loop=360,
            ),
            saturation=PhasedAmplitudeGenerator(
                scale=1.618,
                base=0.6,
                amplitude=0.2
            ),
            light=PhasedAmplitudeGenerator(
                scale=0.618,
                base=0.7,
                amplitude=0.2
            )
        )

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
