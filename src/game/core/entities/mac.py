from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class Mac:
    """Обёртка над bytes MAC"""

    @classmethod
    def broadcast(cls):
        """Широковещательный адрес"""
        return cls(bytes((0xff, 0xff, 0xff, 0xff, 0xff, 0xff)))

    value: bytes

    def __post_init__(self):
        assert len(self.value) == 6

    def __str__(self) -> str:
        return self.value.hex('-', 1)
