from typing import Callable
from typing import Final

from game.core.player import GameInfo
from rs.result import Result
from rs.result import ok
from serialcmd.abc.stream import Stream
from serialcmd.core.protocol import Protocol
from serialcmd.impl.serializer.array_ import ArraySerializer
from serialcmd.impl.serializer.arraystring import ArrayStringSerializer
from serialcmd.impl.serializer.bytearray_ import ByteArraySerializer
from serialcmd.impl.serializer.bytevector import ByteVectorSerializer
from serialcmd.impl.serializer.primitive import u8
from serialcmd.impl.serializer.struct_ import StructSerializer
from serialcmd.impl.serializer.void import VoidSerializer
from serialcmd.impl.stream.byte import ByteBufferInputStream
from serialcmd.impl.stream.byte import ByteBufferOutputStream


class GameProtocol(Protocol):
    mac = ByteArraySerializer(6)

    log_message = ArrayStringSerializer(128)

    espnow_packet = StructSerializer((
        mac,
        ByteVectorSerializer(u8)
    ))

    espnow_delivery_status = StructSerializer((
        mac,
        u8
    ))

    player_message = ArrayStringSerializer(32)
    player_move = ArraySerializer(u8, 2)

    def __init__(self, stream: Stream, game: GameInfo) -> None:
        type Ins[T] = Callable[[T], Result[None, str]]

        super().__init__(stream, u8, u8)
        self.game: Final = game

        self.request_mac: Ins[None] = self.addSender(VoidSerializer())
        self.send_espnow_packet: Ins[tuple[bytes, bytes]] = self.addSender(self.espnow_packet)

        self.addReceiver(self.mac, self._onMac, "read_mac")
        self.addReceiver(self.log_message, self._onLog, "read_log")
        self.addReceiver(self.espnow_packet, self._onEspnowPacket, "read_espnow_packet")
        self.addReceiver(self.espnow_delivery_status, self._onEspnowDeliveryStatus, "read_delivery_status")

    def _onMac(self, mac: bytes):
        self.game.host_mac = mac
        return ok(None)

    def _onLog(self, message: str):
        return ok(self.game.log(f"esp: {message}"))

    def _onEspnowDeliveryStatus(self, packet: tuple[bytes, int]):
        mac, status = packet
        self.mock(status)
        return ok(None)

    def _onEspnowPacket(self, packet: tuple[bytes, bytes]):
        mac, data = packet
        size = len(data)

        stream = ByteBufferInputStream(data)

        if size == 32:
            return (
                self.player_message.read(stream)
                .and_then(lambda message: self._sendEspnowServerMessage(mac, self.game.onPlayerMessage(mac, message)))
                .map_err(lambda e: f"player message err: {e}")
            )

        if size == 2:
            return (
                self.player_move.read(stream)
                .and_then(lambda move: self._sendEspnowServerMessage(mac, self.game.onPlayerMove(mac, move)))
                .map_err(lambda e: f"player move err: {e}")
            )

        return self.send_espnow_packet(f"Invalid client ({mac.hex('-')}) package size: ({size})")

    def _sendEspnowServerMessage(self, mac: bytes, message: str):
        stream = ByteBufferOutputStream()
        return (
            self.log_message.write(stream, message)
            .and_then(lambda _: self.send_espnow_packet((mac, stream.buffer)))
        )
