"""
Protocol
"""
from typing import Final
from typing import Sequence

from game.core.player import GameInfo
from game.core.player import Player
from rs.result import ok
from serialcmd.abc.stream import Stream
from serialcmd.core.protocol import Protocol
from serialcmd.impl.serializer.array_ import ArraySerializer
from serialcmd.impl.serializer.arraystring import ArrayStringSerializer
from serialcmd.impl.serializer.bytearray_ import ByteArraySerializer
from serialcmd.impl.serializer.primitive import u16
from serialcmd.impl.serializer.primitive import u8
from serialcmd.impl.serializer.struct_ import StructSerializer
from serialcmd.impl.serializer.vector import VectorSerializer


class GameProtocolV1(Protocol):
    """Протокол хоста игры (Версия хоста 1)"""

    def __init__(self, stream: Stream, game: GameInfo) -> None:
        super().__init__(stream, u8, u8)

        self.game: Final = game

        mac_serializer = ByteArraySerializer(6)

        player_serializer = StructSerializer((
            mac_serializer,
            ArrayStringSerializer(32),
            u8
        ))

        player_move_serializer = ArraySerializer(u8, 3)

        host_message_serializer = ArrayStringSerializer(128)

        self.addReceiver(u8, lambda _: ok(print(_)))

        self.addReceiver(mac_serializer, self.onMacMessage, "onMac")
        self.addReceiver(host_message_serializer, self.onLogMessage, "onLog")
        self.addReceiver(VectorSerializer(player_move_serializer, u16), self.onBoardUpdate, "onBoard")
        self.addReceiver(VectorSerializer(player_serializer, u16), self.onPlayerListUpdated, "onPlayerList")

    def onMacMessage(self, mac: bytes):
        self.game.players[mac] = Player("GAME-HOST", 2056)
        return ok(None)

    def onLogMessage(self, message: str):
        self.game.logs.append(message)
        return ok(None)

    def onBoardUpdate(self, field: Sequence[tuple[int, int, int]]):
        self.game.field_state.clear()

        for x, y, team in field:
            self.game.field_state[(x, y)] = team

        return ok(None)

    def onPlayerListUpdated(self, players: Sequence[tuple]):
        self.game.players.clear()

        for mac, username, team in players:
            self.game.players[mac] = Player(username, team)

        return ok(None)
