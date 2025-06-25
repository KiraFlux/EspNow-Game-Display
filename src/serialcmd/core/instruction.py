from dataclasses import dataclass

from rs.result import Result
from serialcmd.abc.serializer import Serializable
from serialcmd.abc.serializer import Serializer
from serialcmd.abc.stream import Stream


@dataclass
class Instruction[T: Serializable]:
    """Исполняемая инструкция для отправки/приема данных"""

    stream: Stream
    """Используемый поток"""
    code: bytes
    """Префиксный индекс инструкции"""
    name: str
    """Наименование для отладки и логирования"""
    signature: Serializer[T]
    """Сериализатор для параметров инструкции"""

    def send(self, args: T) -> Result[None, str]:
        """Отправить инструкцию с аргументами в поток"""

    def receive(self) -> Result[T, str]:
        """Принять и десериализовать результат инструкции"""

    def __repr__(self) -> str:
        return f"{self.name}@{self.code.hex()}({self.signature})"
