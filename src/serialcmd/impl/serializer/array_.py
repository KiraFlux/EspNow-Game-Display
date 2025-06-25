from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from rs.result import Result
from rs.result import err
from rs.result import ok
from serialcmd.abc.serializer import Serializable
from serialcmd.abc.serializer import Serializer
from serialcmd.abc.stream import Stream


@dataclass(frozen=True)
class ArraySerializer[T: Serializable](Serializer[Sequence[T]]):
    """Сериализатор массивов фиксированной длины"""

    _item_serializer: Serializer[T]
    """Сериализатор элемента массива"""
    _length: int
    """Длинна массива"""

    def __repr__(self) -> str:
        return f"[{self._length}]{self._item_serializer}"

    def read(self, stream: Stream) -> Result[list, str]:
        items = list()

        for i in range(self._length):
            item_result = self._item_serializer.read(stream)

            if item_result.is_err():
                return item_result.map_err(lambda e: f"Item {i} read error: {e}")

            items.append(item_result.unwrap())

        return ok(items)

    def write(self, stream: Stream, value: list) -> Result[None, str]:
        if len(value) != self._length:
            return err(f"Array length mismatch: expected {self._length}, got {len(value)}")

        for i, item in enumerate(value):
            item_result = self._item_serializer.write(stream, item)

            if item_result.is_err():
                return item_result.map_err(lambda e: f"Item {i} write error: {e}")

        return ok(None)
