from typing import Sequence

from rs.result import Result
from rs.result import err
from rs.result import ok
from serialcmd.abc.serializer import Serializable
from serialcmd.abc.serializer import Serializer


class StructSerializer[T: Sequence[Serializable]](Serializer[T]):
    """Объединение нескольких Serializer"""

    def __init__(self, fields: Sequence[Serializer]) -> None:
        self._fields = fields
        self._size = sum(f.getSize() for f in self._fields)

    def __repr__(self) -> str:
        return f"{{{', '.join(map(str, self._fields))}}}"

    def unpack(self, buffer: bytes) -> Result[T, str]:
        ret = list()
        offset: int = 0

        for field in self._fields:
            unpack = field.unpack(buffer[offset:offset + field.getSize()])

            if unpack.is_err():
                return unpack.map_err(lambda e: f"Field@{offset}: {field} unpack error: {e}")

            offset += field.getSize()

        return ok(ret)

    def pack(self, value: T) -> Result[bytes, str]:
        if (got := len(value)) != (expected := len(self._fields)):
            return err(f"Expected: {expected} ({self}), got {got} ({value}")

        packed_fields = list()

        for index, (field, field_value) in enumerate(zip(self._fields, value)):
            pack = field.pack(field_value)
            field: Serializer

            if pack.is_err():
                return pack.map_err(lambda e: f"Field@{index}: {field} pack error: {e}")

            packed_fields.append(pack.unwrap())

        return ok(b"".join(packed_fields))

    def getSize(self) -> int:
        return self._size
