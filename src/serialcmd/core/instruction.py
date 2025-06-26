from dataclasses import dataclass
from typing import Optional

from rs.result import Result
from serialcmd.abc.serializer import Serializable
from serialcmd.abc.serializer import Serializer
from serialcmd.abc.stream import InputStream
from serialcmd.abc.stream import OutputStream


@dataclass(frozen=True)
class Instruction[T: Serializable]:
    """Исполняемая инструкция протокола"""

    code: bytes
    signature: Serializer[T]
    name: Optional[str]

    def send(self, stream: OutputStream, args: T) -> Result[None, str]:
        """Отправить инструкцию с аргументами в поток"""
        return (
            stream.write(self.code)
            .and_then(lambda _: self.signature.write(stream, args))
            .map_err(lambda e: f"{self.name} send error: {e}")
        )

    def receive(self, stream: InputStream) -> Result[T, str]:
        """Принять и десериализовать результат инструкции"""
        return self.signature.read(stream).map_err(lambda e: f"{self.name} receive error: {e}")

    def __repr__(self) -> str:
        name = self.name or "anonymous"
        return f"{name}@{self.code.hex()}( {self.signature} )"
