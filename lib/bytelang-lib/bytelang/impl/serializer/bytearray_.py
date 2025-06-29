from dataclasses import dataclass

from rs.result import Result
from rs.result import err
from bytelang.abc.serializer import Serializer
from bytelang.abc.stream import InputStream
from bytelang.abc.stream import OutputStream


@dataclass(frozen=True)
class ByteArraySerializer(Serializer[bytes]):
    """Сериализатор байтовых строк"""

    length: int
    """Размер"""

    def __post_init__(self):
        assert self.length >= 1

    def write(self, stream: OutputStream, value: bytes) -> Result[None, str]:
        if len(value) != self.length:
            return err(f"Invalid ByteArray size (expected: {self.length}, got: {len(value)})")

        return (
            stream.write(value)
            .map_err(lambda e: f"{self.write.__name__} error: {e}")
        )

    def read(self, stream: InputStream) -> Result[bytes, str]:
        return (
            stream.read(self.length)
            .map_err(lambda e: f"{self.read.__name__} error: {e}")
        )

    def __repr__(self) -> str:
        return f"[{self.length}]bytes"
