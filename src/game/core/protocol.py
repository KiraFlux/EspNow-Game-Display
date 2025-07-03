from typing import Callable
from typing import Final

from bytelang.abc.stream import Stream
from bytelang.core.protocol import Protocol
from bytelang.impl.serializer.array_ import ArraySerializer
from bytelang.impl.serializer.arraystring import ArrayStringSerializer
from bytelang.impl.serializer.bytearray_ import ByteArraySerializer
from bytelang.impl.serializer.bytevector import ByteVectorSerializer
from bytelang.impl.serializer.primitive import u8
from bytelang.impl.serializer.struct_ import StructSerializer
from bytelang.impl.serializer.void import VoidSerializer
from bytelang.impl.stream.byte import ByteBufferInputStream
from bytelang.impl.stream.byte import ByteBufferOutputStream
from game.core.entities.mac import Mac
from game.core.environment import Environment
from lina.vector import Vector2D
from misc.log import Logger
from rs.result import Result
from rs.result import ok

type Ins[T] = Callable[[T], Result[None, str]]


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

    def __init__(self, stream: Stream, env: Environment) -> None:
        super().__init__(stream, u8, u8)

        self._log = Logger.inst().sub("protocol")
        self._esp_log = self._log.sub("esp")

        self.env: Final = env

        self.request_mac: Ins[None] = self.addSender(VoidSerializer())
        self.send_espnow_packet: Ins[tuple[bytes, bytes]] = self.addSender(self.espnow_packet)

        self.addReceiver(self.mac, self._onMac, "read_mac")
        self.addReceiver(self.log_message, self._onLog, "read_log")
        self.addReceiver(self.espnow_packet, self._onEspnowPacket, "read_espnow_packet")
        self.addReceiver(self.espnow_delivery_status, self._onEspnowDeliveryStatus, "read_delivery_status")

    def _onMac(self, raw_mac: bytes):
        mac = Mac(raw_mac)

        self.env.host_mac = mac

        return ok(self._log.write(f"got host mac: {mac}"))

    def _onLog(self, message: str):
        return ok(self._esp_log.write(message))

    def _onEspnowDeliveryStatus(self, packet: tuple[bytes, int]):
        raw_mac, status = packet

        mac = Mac(raw_mac)
        status_str = "Ok" if status == 0 else "Fail"

        return ok(self._esp_log.write(f"sending to {mac} : {status_str}"))

    def _onEspnowPacket(self, packet: tuple[bytes, bytes]):
        raw_mac, data = packet
        size = len(data)

        mac = Mac(raw_mac)

        stream = ByteBufferInputStream(data)

        if size == 32:
            return (
                self.player_message.read(stream)
                .and_then(lambda message: self._sendEspnowServerMessage(mac, self.env.onPlayerMessage(mac, message)))
                .map_err(lambda e: f"player message err: {e}")
            )

        if size == 2:
            return (
                self.player_move.read(stream)
                .and_then(lambda move: self._sendEspnowServerMessage(mac, self.env.onPlayerMove(mac, Vector2D(*move))))
                .map_err(lambda e: f"player move err: {e}")
            )

        return self._sendEspnowServerMessage(mac, f"Клиент {mac} отправил непредвиденный пакет: ({size} Байт)")

    def _sendEspnowServerMessage(self, mac: Mac, message: str):
        self._log.write(f"send to {mac} : '{message}'")

        stream = ByteBufferOutputStream()
        return (
            self.log_message.write(stream, message)
            .and_then(lambda _: self.send_espnow_packet((mac.value, stream.buffer)))
        )
