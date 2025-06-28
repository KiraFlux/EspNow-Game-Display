from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True, kw_only=True)
class Theme:
    """Тема интерфейса"""

    @classmethod
    def current(cls) -> Theme:
        """Получить текущую тему"""
        return _dark

    background: str
    foreground: str
    secondary_background: str
    accent: str
    border: str
    card_background: str
    muted_text: str


_dark = Theme(
    background="#0A0A12",
    foreground="#F0F0FF",
    secondary_background="#181824",
    accent="#FF6A00",
    border="#334466",
    card_background="#1A1A2A",
    muted_text="#99AABB",
)
