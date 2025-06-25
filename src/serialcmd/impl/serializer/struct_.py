from dataclasses import dataclass
from typing import Sequence

from rs.result import Result
from rs.result import err
from rs.result import ok
from serialcmd.abc.serializer import Serializable
from serialcmd.abc.serializer import Serializer
from serialcmd.abc.stream import InputStream
from serialcmd.abc.stream import OutputStream


@dataclass(frozen=True)
class StructSerializer[T: Sequence[Serializable]](Serializer[T]):
    """Объединение нескольких Serializer"""

    _fields: Sequence[Serializer]
    """Сериализаторы полей структуры"""

    def __repr__(self) -> str:
        return f"{{{', '.join(map(str, self._fields))}}}"

    def read(self, stream: InputStream) -> Result[list, str]:
        values = list()

        for i, field in enumerate(self._fields):
            value = field.read(stream)

            if value.is_err():
                return err(f"Field {i} error: {value.err().unwrap()}")

            values.append(value.unwrap())

        return ok(values)

    def write(self, stream: OutputStream, value: list) -> Result[None, str]:
        if len(value) != len(self._fields):
            return err(f"Value/fields count mismatch: {len(value)} vs {len(self._fields)}")

        for i, (field, item) in enumerate(zip(self._fields, value)):
            result = field.write(stream, item)

            if result.is_err():
                return err(f"Field {i} write error: {result.unwrap()}")

        return ok(None)
