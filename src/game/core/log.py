from __future__ import annotations

from typing import ClassVar
from typing import Optional


class Logger:
    """Иерархический лог"""

    _inst: ClassVar[Optional[Logger]] = None
    _messages: ClassVar = list[str]()
    _key = "root"

    def write(self, message: str) -> None:
        """Записать сообщение в лог"""
        self._messages.append(f"[{self._key}]: {message}")

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


class SubLogger(Logger):
    """Дочерний лог"""

    def __init__(self, parent: Logger, key: str) -> None:
        self._parent = parent
        self._key: str = f"{parent._key}::{key}"
