from rs.result import Result
from rs.result import ok
from bytelang.abc.serializer import Serializer
from bytelang.abc.stream import InputStream
from bytelang.abc.stream import OutputStream


class VoidSerializer(Serializer[None]):
    def read(self, stream: InputStream) -> Result[None, str]:
        return ok(None)

    def write(self, stream: OutputStream, value: None) -> Result[None, str]:
        return ok(None)

    def __repr__(self) -> str:
        return "void"
