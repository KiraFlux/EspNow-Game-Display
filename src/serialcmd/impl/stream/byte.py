from dataclasses import dataclass
from dataclasses import field

from rs.result import Result
from rs.result import err
from rs.result import ok
from serialcmd.abc.stream import InputStream
from serialcmd.abc.stream import OutputStream


@dataclass
class ByteBufferInputStream(InputStream):
    """Поток ввода, работающий с буфером байтов в памяти."""

    _data: bytes
    _index: int = field(default=0, init=False)

    def read(self, size: int) -> Result[bytes, str]:
        """
        Считывает указанное количество байтов из буфера.

        Args:
            size: Количество байтов для чтения (должно быть положительным)

        Returns:
            Result с прочитанными данными или описанием ошибки
        """

        if size < 0:
            return err(f"Invalid read size: {size}. Size must be non-negative")

        if self._index >= len(self._data):
            return err("Read beyond end of buffer")

        # Вычисляем доступные данные
        available = len(self._data) - self._index
        read_size = min(size, available)

        # Читаем данные и обновляем позицию
        result = self._data[self._index:self._index + read_size]
        self._index += read_size

        return ok(result)

    def available(self) -> int:
        """Возвращает количество доступных для чтения байтов"""
        return len(self._data) - self._index

    def reset(self) -> None:
        """Сбрасывает позицию чтения в начало буфера"""
        self._index = 0


@dataclass(frozen=True)
class ByteBufferOutputStream(OutputStream):
    """
    Поток вывода, записывающий данные в буфер в памяти.

    Реализован как неизменяемый dataclass с прямым доступом к буферу.
    Полезен для тестирования и сбора выходных данных.
    """

    buffer: bytearray = field(default_factory=bytearray, init=False)

    def write(self, data: bytes) -> Result[None, str]:
        """
        Записывает данные в буфер.

        Args:
            data: Байтовые данные для записи

        Returns:
            Успешный Result или ошибку, если данные не являются bytes
        """

        if not isinstance(data, bytes):
            return err(f"Invalid data type: {type(data)}. Expected bytes")

        return ok(self.buffer.extend(data))
