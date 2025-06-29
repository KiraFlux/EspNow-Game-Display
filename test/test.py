from rs.result import ok
from bytelang.abc.stream import Stream
from bytelang.core import Protocol
from bytelang.impl.serializer import PrimitiveSerializer
from bytelang.impl.serializer import u8
from bytelang.impl.serializer import StructSerializer
from bytelang.impl import VirtualStream

_game_stream, _device_stream = VirtualStream.create_pair()

client_move = StructSerializer((u8, u8))


class GameProtocol(Protocol):

    def __init__(self, stream: Stream, local_code: PrimitiveSerializer[int], remote_code: PrimitiveSerializer[int]) -> None:
        super().__init__(stream, local_code, remote_code)

        self.set_field_size = self.addSender(client_move, "setFieldSize").unwrap()


class DeviceProtocol(Protocol):

    def __init__(self, stream: Stream, local_code: PrimitiveSerializer[int], remote_code: PrimitiveSerializer[int]) -> None:
        super().__init__(stream, local_code, remote_code)

        self.addReceiver(client_move, lambda args: ok(print(args)), "onFieldSize")


game = GameProtocol(_game_stream, u8, u8)
device = DeviceProtocol(_device_stream, u8, u8)

game.set_field_size.send(_game_stream, (15, 15))

print(f"""
RX: {_device_stream.rx.hex(' ')}
TX: {_device_stream.tx.hex(' ')}
""")
