from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from rs.result import Result
from rs.result import err
from rs.result import ok
from bytelang.abc.serializer import Serializable
from bytelang.abc.serializer import Serializer
from bytelang.abc.stream import InputStream
from bytelang.abc.stream import OutputStream


@dataclass(frozen=True)
class ArraySerializer[T: Serializable](Serializer[Sequence[T]]):
    """Сериализатор массивов фиксированной длины"""

    item: Serializer[T]
    """Сериализатор элемента массива"""
    length: int
    """Длинна массива"""

    def __post_init__(self):
        assert self.length >= 1

    def __repr__(self) -> str:
        return f"[{self.length}]{self.item}"

    def read(self, stream: InputStream) -> Result[list, str]:
        items = list()

        for i in range(self.length):
            item_result = self.item.read(stream)

            if item_result.is_err():
                return item_result.map_err(lambda e: f"Item {i} read error: {e}")

            items.append(item_result.unwrap())

        return ok(items)

    def write(self, stream: OutputStream, value: list) -> Result[None, str]:
        if len(value) != self.length:
            return err(f"Array length mismatch: expected {self.length}, got {len(value)}")

        for i, item in enumerate(value):
            item_result = self.item.write(stream, item)

            if item_result.is_err():
                return item_result.map_err(lambda e: f"Item {i} write error: {e}")

        return ok(None)
