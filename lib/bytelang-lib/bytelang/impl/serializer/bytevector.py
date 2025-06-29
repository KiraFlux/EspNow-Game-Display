from dataclasses import dataclass

from rs.result import Result
from bytelang.abc.serializer import Serializer
from bytelang.abc.stream import InputStream
from bytelang.abc.stream import OutputStream
from bytelang.impl.serializer.primitive import PrimitiveSerializer


@dataclass(frozen=True)
class ByteVectorSerializer(Serializer[bytes]):
    """Вектор байт"""

    length: PrimitiveSerializer[int]
    """Примитив длины"""

    def write(self, stream: OutputStream, value: bytes) -> Result[None, str]:
        len_result = self.length.write(stream, len(value))

        if len_result.is_err():
            return len_result.map_err(lambda e: f"{self.write} (len) err: {e}")

        return (
            stream.write(value)
            .map_err(lambda e: f"{self.write} err: {e}")
        )

    def read(self, stream: InputStream) -> Result[bytes, str]:
        return (
            self.length.read(stream)
            .and_then(lambda length: stream.read(length))
            .map_err(lambda e: f"{self.read} error: {e}")
        )

    def __repr__(self) -> str:
        return f"[{self.length}]bytes"
