from abc import ABC
from abc import abstractmethod

from rs.result import Result


class Stream(ABC):
    """Абстрактный базовый класс для потоков ввода-вывода байтов"""

    @abstractmethod
    def write(self, data: bytes) -> Result[None, str]:
        """Записать данные в поток вывода"""

    @abstractmethod
    def read(self, size: int) -> Result[bytes, str]:
        """Считать данные из потока ввода"""
