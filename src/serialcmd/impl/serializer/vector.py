from dataclasses import dataclass
from typing import Sequence

from rs.result import Result
from rs.result import ok
from serialcmd.abc.serializer import Serializer
from serialcmd.abc.stream import InputStream
from serialcmd.abc.stream import OutputStream
from serialcmd.impl.serializer.primitive import PrimitiveSerializer


@dataclass(frozen=True, kw_only=True)
class VectorSerializer[T](Serializer[Sequence[T]]):
    """Сериализатор динамического массива"""

    length: PrimitiveSerializer[int]
    """Примитив описывающий длину"""
    item: Serializer[T]
    """Сериализатор элемента"""

    def read(self, stream: InputStream) -> Result[Sequence[T], str]:
        # Чтение длины вектора
        length_result = self.length.read(stream)

        if length_result.is_err():
            # noinspection PyTypeChecker
            return length_result.map_err(lambda e: f"Length read error: {e}")

        length = length_result.unwrap()
        items = list()

        # Чтение элементов
        for i in range(length):
            item_result = self.item.read(stream)

            if item_result.is_err():
                return item_result.map_err(lambda e: f"Item {i} read error: {e}")

            items.append(item_result.unwrap())

        return ok(items)

    def write(self, stream: OutputStream, value: Sequence[T]) -> Result[None, str]:
        length = len(value)
        len_result = self.length.write(stream, length)

        if len_result.is_err():
            return len_result.map_err(lambda e: f"Length write error: {e}")

        for i, item in enumerate(value):
            item_result = self.item.write(stream, item)

            if item_result.is_err():
                return item_result.map_err(lambda e: f"Item {i} write error: {e}")

        return ok(None)

    def __repr__(self) -> str:
        return f"[{self.length}]{self.item}"
