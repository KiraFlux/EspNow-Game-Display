from dataclasses import dataclass
from typing import Iterable

import serial.tools.list_ports
from serial import Serial as SerialPort

from serialcmd.abc.stream import Stream


@dataclass
class Serial(Stream):
    """Стрим по последовательному порту"""

    def __init__(self, port: str, baud: int) -> None:
        self._serial_port = SerialPort(port=port, baudrate=baud, timeout=None)

    def read(self, size: int = 1) -> bytes:
        return self._serial_port.read(size)

    def write(self, data: bytes) -> None:
        self._serial_port.write(data)

    @staticmethod
    def getPorts(keywords: Iterable[str] = ("Arduino", "CH340", "USB-SERIAL")) -> list[str]:
        """
        Находит порты, содержащие указанные ключевые слова в описании устройства.
        @param keywords: Список ключевых слов для поиска (по умолчанию ищет Arduino).
        """
        return [
            port.device for port in serial.tools.list_ports.comports()
            if any(keyword in port.description for keyword in keywords)
        ]

    def __str__(self) -> str:
        return f"{self.__class__.__name__}<{self._serial_port.port}>"
