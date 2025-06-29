from dataclasses import dataclass
from typing import Optional

from rs.result import Result
from bytelang.abc.serializer import Serializable
from bytelang.abc.serializer import Serializer
from bytelang.abc.stream import InputStream
from bytelang.abc.stream import OutputStream


@dataclass(frozen=True)
class Instruction[T: Serializable]:
    """Исполняемая инструкция протокола"""

    code: bytes
    signature: Serializer[T]
    name: Optional[str]

    def send(self, stream: OutputStream, value: T) -> Result[None, str]:
        """Отправить инструкцию с аргументами в поток"""
        return (
            stream.write(self.code)
            .and_then(lambda _: self.signature.write(stream, value))
            .map_err(lambda e: f"{self.name} send error: {e}")
        )

    def receive(self, stream: InputStream) -> Result[T, str]:
        """Принять и десериализовать результат инструкции"""
        return self.signature.read(stream).map_err(lambda e: f"{self.name} receive error: {e}")

    def __repr__(self) -> str:
        name = self.name or "anonymous"
        return f"{name}@{self.code.hex()}( {self.signature} )"
