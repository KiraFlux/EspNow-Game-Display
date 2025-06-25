"""
Protocol
"""

from typing import Sequence

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

    def __init__(self, stream: Stream) -> None:
        super().__init__(stream, u8, u8)

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
        print(f"mac: {mac.hex('-')}")

        return ok(None)

    def onLogMessage(self, message: str):
        print(f"log: {message}")

        return ok(None)

    def onBoardUpdate(self, field: Sequence[tuple[int, int, int]]):
        for x, y, team in field:
            print(f"{x, y}: {team}")

        return ok(None)

    def onPlayerListUpdated(self, players: Sequence[tuple]):
        for mac, username, team in players:
            print(f"{mac=} {username=} {team=}")

        return ok(None)
