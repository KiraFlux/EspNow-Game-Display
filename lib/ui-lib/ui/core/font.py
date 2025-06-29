from typing import Final


class FontFactory:
    """Фабрика для создания согласованных шрифтов"""
    base_font: Final = "Segoe UI"
    mono_font: Final = "Consolas"

    @classmethod
    def heading(cls) -> tuple[str, int, str]:
        """Шрифт для заголовков"""
        return cls.base_font, 14, "bold"

    @classmethod
    def body(cls) -> tuple[str, int, str]:
        """Основной шрифт для текста"""
        return cls.base_font, 11, "normal"

    @classmethod
    def mono(cls) -> tuple[str, int, str]:
        """Моноширинный шрифт для логов"""
        return cls.mono_font, 10, "normal"

    @classmethod
    def small(cls) -> tuple[str, int, str]:
        """Мелкий текст"""
        return cls.base_font, 9, "normal"
