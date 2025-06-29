from __future__ import annotations

from dataclasses import dataclass

from misc.color import Color


@dataclass(frozen=True, kw_only=True)
class Theme:
    """Тема интерфейса"""

    background: Color
    foreground: Color
    secondary_background: Color
    accent: Color
    border: Color
    card_background: Color
    muted_text: Color

    @classmethod
    def current(cls) -> Theme:
        """Получить текущую тему"""
        return _dark

    @classmethod
    def dark(cls) -> Theme:
        """Создать тёмную тему"""
        orange = Color.fromHex("#FF6A00")
        blue = Color.fromHex("#334466")

        background = Color.gray(0.1)
        secondary_background = background.brighter()
        card_background = secondary_background.brighter()

        foreground = Color.gray(0.9)
        muted_text = foreground.darker()

        return cls(
            background=background,
            foreground=foreground,
            secondary_background=secondary_background,
            accent=orange,
            border=blue,
            card_background=card_background,
            muted_text=muted_text,
        )


_dark = Theme.dark()
