from rs.result import Result
from serialcmd.abc.stream import Stream


class MockStream(Stream):
    """Заглушка для тестирования"""

    def write(self, data: bytes) -> Result[None, str]:
        pass

    def read(self, size: int) -> Result[bytes, str]:
        pass
