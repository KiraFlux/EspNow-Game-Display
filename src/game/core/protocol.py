from game.core.player import GameInfo
from serialcmd.abc.stream import Stream
from serialcmd.core.protocol import Protocol
from serialcmd.impl.serializer.arraystring import ArrayStringSerializer
from serialcmd.impl.serializer.bytearray_ import ByteArraySerializer
from serialcmd.impl.serializer.bytevector import ByteVectorSerializer
from serialcmd.impl.serializer.primitive import u8
from serialcmd.impl.serializer.struct_ import StructSerializer
from serialcmd.impl.serializer.void import VoidSerializer


class GameProtocolV2(Protocol):

    def __init__(self, stream: Stream, game: GameInfo) -> None:
        super().__init__(stream, u8, u8)
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

        self.addReceiver(mac, self.mock, "read_mac")
        self.addReceiver(log, self.mock, "read_log")
        self.addReceiver(espnow_packet, self.mock, "read_espnow_packet")
        self.addReceiver(delivery_status, self.mock, "read_delivery_status")
