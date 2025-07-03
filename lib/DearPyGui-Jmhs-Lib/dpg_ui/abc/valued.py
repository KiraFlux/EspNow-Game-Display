from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass


@dataclass(kw_only=True)
class Valued[T](ABC):
    """Содержит значение"""

    _value_default: T
    """Значение по умолчанию"""

    @abstractmethod
    def setValue(self, value: T) -> None:
        """Установить значение"""

    @abstractmethod
    def getValue(self) -> T:
        """Получить актуальное значение"""
