from dataclasses import dataclass

from rs.result import Result
from rs.result import err
from serialcmd.abc.serializer import Serializer
from serialcmd.abc.stream import InputStream
from serialcmd.abc.stream import OutputStream
from serialcmd.impl.serializer.primitive import PrimitiveSerializer


@dataclass(frozen=True)
class ByteVectorSerializer(Serializer[bytes]):
    """Вектор байт"""

    length: PrimitiveSerializer[int]
    """Примитив длины"""

    def write(self, stream: OutputStream, value: bytes) -> Result[None, str]:
        len_result = self.length.write(stream, len(value))

        if len_result.is_err():
            return len_result.map_err(lambda e: f"{self.write} (len) err: {e}")

        if len_result.unwrap() != len(value):
            return err(f"Invalid len: {len_result.unwrap()} vs {len(value)}")

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
