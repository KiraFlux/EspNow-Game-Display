from abc import ABC
from abc import abstractmethod
from typing import Sequence

from rs.result import Result
from serialcmd.abc.stream import InputStream
from serialcmd.abc.stream import OutputStream

type _serializable = int | float
type _serializable = Sequence[_serializable] | _serializable
type _serializable = Sequence[_serializable] | _serializable

Serializable = _serializable


class Serializer[T: Serializable](ABC):
    """Serializer - упаковка, распаковка данных"""

    @abstractmethod
    def read(self, stream: InputStream) -> Result[T, str]:
        """Считать значение из потока"""

    @abstractmethod
    def write(self, stream: OutputStream, value: T) -> Result[None, str]:
        """Записать значение в поток"""
