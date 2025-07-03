from __future__ import annotations

from typing import Callable
from typing import ClassVar
from typing import Iterable
from typing import MutableMapping
from typing import MutableSequence
from typing import Optional
from typing import Sequence


class Logger:
    """Иерархический лог"""

    _inst: ClassVar[Optional[Logger]] = None
    _logs: ClassVar[MutableMapping[str, MutableSequence[tuple[int, str]]]] = dict()
    _writes: ClassVar = 0

    on_write: ClassVar[Optional[Callable[[], None]]] = None
    on_create: ClassVar[Optional[Callable[[str], None]]] = None

    def __init__(self, key: str) -> None:
        super().__init__()
        self._key = key

        if self.on_create is not None:
            self.on_create(key)

        self.write("created")

    def write(self, message: str) -> None:
        """Записать сообщение в лог"""

        out = self._logs.get(self._key)

        if out is None:
            out = self._logs[self._key] = list()

        out.append((
            self._writes,
            message
        ))

        self.__class__._writes += 1

        if self.on_write is not None:
            self.on_write()

    def sub(self, key: str) -> Logger:
        """Создать дочерний лог"""
        return Logger(f"{self._key}::{key}")

    @classmethod
    def inst(cls) -> Logger:
        """Возвращает экземпляр родительского лога"""

        if cls._inst is None:
            cls._inst = Logger("root")

        return cls._inst

    @classmethod
    def getKeys(cls) -> Sequence[str]:
        """Получить все доступные ключи журнала"""
        return tuple(cls._logs.keys())

    @classmethod
    def getByFilter(cls, keys: Sequence[str]) -> Iterable[str]:
        """Получить логи"""
        if len(keys) == 0:
            return ()

        entries = (
            (index, key, msg)
            for key in keys
            if key in cls._logs
            for index, msg in cls._logs[key]
        )

        padding = max(map(len, keys)) + 2

        sorted_entries = sorted(entries, key=lambda x: x[0])

        return (
            f"{f"[{key}]":{padding}} {msg}"
            for _, key, msg in sorted_entries
        )
