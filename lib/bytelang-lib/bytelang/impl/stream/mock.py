from rs.result import Result
from rs.result import ok
from bytelang.abc.stream import Stream


class MockStream(Stream):

    def write(self, data: bytes) -> Result[None, str]:
        return ok(None)

    def read(self, size: int) -> Result[bytes, str]:
        return ok(bytes(size))
