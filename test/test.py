from rs.result import ok
from serialcmd.abc.stream import Stream
from serialcmd.core.protocol import Protocol
from serialcmd.impl.serializer.primitive import PrimitiveSerializer
from serialcmd.impl.serializer.primitive import u8
from serialcmd.impl.serializer.struct_ import StructSerializer
from serialcmd.impl.stream.mock import MockStream

_game_stream, _device_stream = MockStream.create_pair()

client_move = StructSerializer((u8, u8))


class GameProtocol(Protocol):

    def __init__(self, stream: Stream, local_code: PrimitiveSerializer[int], remote_code: PrimitiveSerializer[int]) -> None:
        super().__init__(stream, local_code, remote_code)

        self.set_field_size = self.addSender("setFieldSize", client_move).unwrap()


class DeviceProtocol(Protocol):

    def __init__(self, stream: Stream, local_code: PrimitiveSerializer[int], remote_code: PrimitiveSerializer[int]) -> None:
        super().__init__(stream, local_code, remote_code)

        self.addReceiver("onFieldSize", client_move, lambda args: ok(print(args)))


game = GameProtocol(_game_stream, u8, u8)
device = DeviceProtocol(_device_stream, u8, u8)

game.set_field_size.send(_game_stream, (15, 15))

print(f"""
RX: {_device_stream.rx.hex(' ')}
TX: {_device_stream.tx.hex(' ')}
""")
