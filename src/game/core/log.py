from __future__ import annotations

from typing import ClassVar
from typing import Optional


class Logger:
    """Иерархический лог"""

    _inst: ClassVar[Optional[Logger]] = None
    _messages: ClassVar = list[str]()

    _key = "root"
    _max_key_length: ClassVar = len(_key)

    def write(self, message: str) -> None:
        """Записать сообщение в лог"""
        key = f"[{self._key}]"
        self._messages.append(f"{key:{self._max_key_length}}: {message}")

    def sub(self, key: str) -> Logger:
        """Создать дочерний лог"""
        return SubLogger(self, key)

    @classmethod
    def inst(cls) -> Logger:
        """Возвращает экземпляр родительского лога"""

        if cls._inst is None:
            cls._inst = Logger()

        return cls._inst

    @classmethod
    def available(cls) -> bool:
        """Содержит доступные сообщения"""
        return bool(cls._messages)

    @classmethod
    def read(cls) -> str:
        """Прочесть и удалить"""
        return cls._messages.pop(0)

    @classmethod
    def _updateKeyLength(cls, key: str) -> None:
        cls._max_key_length = max(len(key) + 2, cls._max_key_length)


class SubLogger(Logger):
    """Дочерний лог"""

    def __init__(self, parent: Logger, key: str) -> None:
        self._parent = parent
        self._key: str = f"{parent._key}::{key}"

        self._updateKeyLength(self._key)
