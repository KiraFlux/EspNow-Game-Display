from abc import ABC
from abc import abstractmethod

from rs.result import Result


class InputStream(ABC):
    """Абстрактный поток ввода (чтения)"""

    @abstractmethod
    def read(self, size: int) -> Result[bytes, str]:
        """Считать данные из потока ввода"""


class OutputStream(ABC):
    """Абстрактный поток вывода (записи)"""

    @abstractmethod
    def write(self, data: bytes) -> Result[None, str]:
        """Записать данные в поток вывода"""


class Stream(InputStream, OutputStream, ABC):
    """Поток ввода-вывода"""
