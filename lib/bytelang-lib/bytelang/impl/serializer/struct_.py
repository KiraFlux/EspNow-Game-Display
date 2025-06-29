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
class StructSerializer[T: Sequence[Serializable]](Serializer[T]):
    """Объединение нескольких Serializer"""

    fields: Sequence[Serializer]

    def __repr__(self) -> str:
        return f"{{ {', '.join(map(str, self.fields))} }}"

    def read(self, stream: InputStream) -> Result[T, str]:
        values = list()

        for i, field in enumerate(self.fields):
            value = field.read(stream)

            if value.is_err():
                return err(f"Field {i} error: {value.err().unwrap()}")

            values.append(value.unwrap())

        return ok(values)

    def write(self, stream: OutputStream, value: T) -> Result[None, str]:
        if len(value) != len(self.fields):
            return err(f"Value/fields count mismatch: {len(value)} vs {len(self.fields)}")

        for i, (field, item) in enumerate(zip(self.fields, value)):
            result = field.write(stream, item)

            if result.is_err():
                return err(f"Field {i} write error: {result}")

        return ok(None)
