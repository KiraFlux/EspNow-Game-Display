from serialcmd.core.protocol import Protocol
from serialcmd.impl.serializer.primitive import f32
from serialcmd.impl.serializer.primitive import u8
from serialcmd.impl.serializer.struct_ import StructSerializer
from serialcmd.impl.stream.mock import MockStream

p = Protocol(
    _stream=MockStream(),
    _local_instruction_code=u8,
    _remote_instruction_code=u8
)

vec2 = StructSerializer((u8, u8))

p.registerSender("set_board_size", vec2)
p.registerSender("set_player_send_timeout", f32)

print('\n'.join(map(str, p.getSenders())))
print('\n'.join(map(str, p.getReceivers())))
