from dataclasses import dataclass

from rs.result import Result
from serialcmd.abc.serializer import Serializable
from serialcmd.abc.serializer import Serializer
from serialcmd.abc.stream import Stream


@dataclass
class Instruction[T: Serializable]:
    """Исполняемая инструкция для отправки/приема данных"""

    code: bytes
    """Префиксный индекс инструкции"""
    name: str
    """Наименование для отладки и логирования"""
    signature: Serializer[T]
    """Сериализатор для параметров инструкции"""

    def pack(self, args: T) -> Result[bytes, str]:
        """Упаковать аргументы в байтовую последовательность"""
        return (
            self.signature.pack(args)
            .map(lambda data: self.code + data)
            .map_err(lambda e: f"Instruction pack error: {e}")
        )

    def send(self, stream: Stream, args: T) -> Result[None, str]:
        """Отправить инструкцию с аргументами в поток"""
        return (
            self.pack(args)
            .and_then(lambda data: stream.write(data))
            .map_err(lambda e: f"Instruction send error: {e}")
        )

    def receive(self, stream: Stream) -> Result[T, str]:
        """Принять и десериализовать результат инструкции"""
        return (
            stream.read(self.signature.getSize())
            .and_then(lambda data: self.signature.unpack(data))
            .map_err(lambda e: f"Instruction receive error: {e}")
        )

    def __repr__(self) -> str:
        return f"{self.name}@{self.code.hex()}({self.signature})"
