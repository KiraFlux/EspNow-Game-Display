from __future__ import annotations

from dataclasses import dataclass

from game.ui.color import Color


@dataclass(frozen=True, kw_only=True)
class Theme:
    """Тема интерфейса"""

    @classmethod
    def current(cls) -> Theme:
        """Получить текущую тему"""
        return _dark

    background: Color
    foreground: Color
    secondary_background: Color
    accent: Color
    border: Color
    card_background: Color
    muted_text: Color


_dark = Theme(
    background=Color.fromHex("#0A0A12"),
    foreground=Color.fromHex("#F0F0FF"),
    secondary_background=Color.fromHex("#181824"),
    accent=Color.fromHex("#FF6A00"),
    border=Color.fromHex("#334466"),
    card_background=Color.fromHex("#1A1A2A"),
    muted_text=Color.fromHex("#99AABB"),
)
