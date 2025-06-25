from dataclasses import dataclass
from typing import Sequence

import serial.tools.list_ports
from serial import Serial as SerialPort

from rs.result import Result
from rs.result import err
from rs.result import ok
from serialcmd.abc.stream import InputStream
from serialcmd.abc.stream import OutputStream


@dataclass
class SerialStream(InputStream, OutputStream):
    """Потом ввода-вывода по последовательному порту"""

    def __init__(self, port: str, baud: int) -> None:
        self._serial_port = SerialPort(port=port, baudrate=baud, timeout=None)

    def read(self, size: int) -> Result[bytes, str]:
        try:
            return ok(self._serial_port.read(size))

        except Exception as e:
            return err(f"SerialStream read error: {e}")

    def write(self, data: bytes) -> Result[None, str]:
        # noinspection PyBroadException
        try:
            ok(self._serial_port.write(data))

        except Exception as e:
            return err(f"SerialStream write error: {e}")

    @staticmethod
    def getPorts(keywords: Sequence[str] = ("Arduino", "CH340", "USB-SERIAL")) -> list[str]:
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
