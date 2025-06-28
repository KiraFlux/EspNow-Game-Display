from typing import Final


class FontFactory:
    """Фабрика для создания согласованных шрифтов"""
    BASE_FONT: Final = "Segoe UI"
    MONO_FONT: Final = "Consolas"

    @classmethod
    def heading(cls) -> tuple[str, int, str]:
        """Шрифт для заголовков"""
        return cls.BASE_FONT, 14, "bold"

    @classmethod
    def body(cls) -> tuple[str, int, str]:
        """Основной шрифт для текста"""
        return cls.BASE_FONT, 11, "normal"

    @classmethod
    def mono(cls) -> tuple[str, int, str]:
        """Моноширинный шрифт для логов"""
        return cls.MONO_FONT, 10, "normal"

    @classmethod
    def small(cls) -> tuple[str, int, str]:
        """Мелкий текст"""
        return cls.BASE_FONT, 9, "normal"
