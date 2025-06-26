from typing import Final

from game.core.player import GameInfo
from rs.result import ok
from serialcmd.abc.stream import Stream
from serialcmd.core.protocol import Protocol
from serialcmd.impl.serializer.arraystring import ArrayStringSerializer
from serialcmd.impl.serializer.bytearray_ import ByteArraySerializer
from serialcmd.impl.serializer.bytevector import ByteVectorSerializer
from serialcmd.impl.serializer.primitive import u8
from serialcmd.impl.serializer.struct_ import StructSerializer
from serialcmd.impl.serializer.void import VoidSerializer


class GameProtocol(Protocol):

    def __init__(self, stream: Stream, game: GameInfo) -> None:
        super().__init__(stream, u8, u8)
        self._game: Final = game

        mac = ByteArraySerializer(6)
        log = ArrayStringSerializer(128)

        espnow_packet = StructSerializer((
            mac,
            ByteVectorSerializer(u8)
        ))

        delivery_status = StructSerializer((
            mac,
            u8
        ))

        self.request_mac = self.addSender(VoidSerializer())
        self.send_espnow_packet = self.addSender(espnow_packet)

        self.addReceiver(mac, self._onMac, "read_mac")
        self.addReceiver(log, self._onLog, "read_log")
        self.addReceiver(espnow_packet, self._onEspnowPacket, "read_espnow_packet")
        self.addReceiver(delivery_status, self._onEspnowDeliveryStatus, "read_delivery_status")

    def _onMac(self, mac: bytes):
        self._game.host_mac = mac
        return ok(None)

    def _onLog(self, message: str):
        self._game.logs.append(message)
        return ok(None)

    def _onEspnowPacket(self, packet: tuple[bytes, bytes]):
        self.mock(packet)
        return ok(None)

    def _onEspnowDeliveryStatus(self, status: tuple[bytes, int]):
        self.mock(status)
        return ok(None)
