from rs.result import Result
from rs.result import err
from rs.result import ok
from serialcmd.abc.serializer import Serializer
from serialcmd.abc.stream import InputStream
from serialcmd.abc.stream import OutputStream
from serialcmd.impl.serializer.bytearray_ import ByteArraySerializer


class ArrayStringSerializer(Serializer[str]):
    """Сериализатор строк фиксированной длины с UTF-8 кодировкой"""

    def __init__(self, length: int) -> None:
        self._byte_array_serializer = ByteArraySerializer(length)

    def write(self, stream: OutputStream, value: str) -> Result[None, str]:
        """Записать строку как байты фиксированной длины"""
        try:
            encoded = value.encode('utf-8')

            if len(encoded) > self._byte_array_serializer.length:
                return err(f"String too long ({len(encoded)} > {self._byte_array_serializer.length} bytes)")

            padded = encoded + b'\x00' * (self._byte_array_serializer.length - len(encoded))
            return self._byte_array_serializer.write(stream, padded)

        except Exception as e:
            return err(f"{self.write.__name__} error: {str(e)}")

    def read(self, stream: InputStream) -> Result[str, str]:
        """Прочитать строку из байтов фиксированной длины"""
        try:
            data = self._byte_array_serializer.read(stream)

            if data.is_err():
                return err(data.err().unwrap())

            return ok(data.unwrap().rstrip(b'\x00').decode('utf-8'))

        except Exception as exception:
            return err(f"{self.read.__name__} error: {exception}")
    
    def __repr__(self) -> str:
        return f"[{self._byte_array_serializer.length}]str"
