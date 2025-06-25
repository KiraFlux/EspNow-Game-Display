from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from rs.result import Result
from rs.result import err
from rs.result import ok
from serialcmd.abc.serializer import Serializable
from serialcmd.abc.serializer import Serializer


@dataclass(frozen=True)
class ArraySerializer[T: Serializable](Serializer[Sequence[T]]):
    """Сериализатор однородной структуры (Массив)"""

    _item_serializer: Serializer[T]
    """Сериализатор элемента массива"""
    _length: int
    """Длинна массива"""

    @classmethod
    def new(cls, item: Serializer[T], length: int) -> Result[ArraySerializer, str]:
        """Создать массив с проверкой"""
        if length < 1:
            return err(f"Invalid array length: {length}")

        return ok(cls(item, length))

    def unpack(self, buffer: bytes) -> Result[T, str]:
        ret = list()

        offset: int = 0

        for i in range(self._length):
            unpack = self._item_serializer.unpack(buffer[offset:offset + self._item_serializer.getSize()])

            if unpack.is_err():
                return unpack.map_err(lambda e: f"array element at {i} unpack error: {e}")

            ret.append(unpack.unwrap())
            offset += self._item_serializer.getSize()

        return ok(ret)

    def pack(self, value: T) -> Result[bytes, str]:
        if (got := len(value)) != self._length:
            return err(f"Expected: {self._length} ({self}), got {got} ({value}")

        ret = list()

        for index, field_value in enumerate(value):
            pack = self._item_serializer.pack(field_value)

            if pack.is_err():
                return pack.map_err(lambda e: f"Field@{index}: pack error: {e}")

            ret.append(pack.unwrap())

        return ok(b"".join(ret))

    def getSize(self) -> int:
        return self._item_serializer.getSize() * self._length

    def __repr__(self) -> str:
        return f"[{self._length}]{self._item_serializer}"
