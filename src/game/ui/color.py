import math
from dataclasses import dataclass
from functools import cache
from typing import Final
from typing import Self


@dataclass(frozen=True)
class Color:
    """Цвет"""
    r: int
    g: int
    b: int

    @classmethod
    def fromHex(cls, _hex: str) -> Self:
        """Создать цвет на основе HEX строки"""
        assert len(_hex) == 7
        assert _hex[0] == '#'
        r = int(_hex[1:3], 16)
        g = int(_hex[3:5], 16)
        b = int(_hex[5:7], 16)
        return cls(r, g, b)

    def hex(self) -> str:
        """Преобразовать в HEX представление"""
        return f"#{self.r:02x}{self.g:02x}{self.b:02x}"

    def brightness(self) -> float:
        """Вычислить нормализованную яркость"""
        return 0.2126 * self.r + 0.7152 * self.g + 0.0722 * self.b


white: Final = Color.fromHex("#ffffff")
black: Final = Color.fromHex("#000000")

# Константы для генерации цветов
GOLDEN_RATIO = (1 + math.sqrt(5)) / 2
HUE_START = 15  # Начальный оттенок (оранжевый)
HUE_STEP = 360 / GOLDEN_RATIO  # Шаг оттенка (~222.5°)
TARGET_BRIGHTNESS = 200  # Целевая яркость (0-255)
INITIAL_SATURATION = 0.6  # Насыщенность для пастельных тонов
INITIAL_LIGHTNESS = 0.8  # Начальная светлота


def _hsl_to_rgb(h: float, s: float, l: float) -> tuple[int, int, int]:
    """Преобразование HSL в RGB"""
    if s == 0:
        r = g = b = l

    else:
        def _hue_to_rgb(p: float, q: float, t: float) -> float:
            t %= 1.0

            if t < 0:
                t += 1

            if t < 1 / 6:
                return p + (q - p) * 6 * t

            if t < 0.5:
                return q

            if t < 2 / 3:
                return p + (q - p) * (2 / 3 - t) * 6

            return p

        h_norm = h / 360.0
        q = l * (1 + s) if l < 0.5 else l + s - l * s
        p = 2 * l - q
        r = _hue_to_rgb(p, q, h_norm + 1 / 3)
        g = _hue_to_rgb(p, q, h_norm)
        b = _hue_to_rgb(p, q, h_norm - 1 / 3)

    return round(r * 255), round(g * 255), round(b * 255)


@cache
def get_team_color(team: int) -> Color:
    """Генерация уникального цвета для команды"""
    hue = (HUE_START + (team - 1) * HUE_STEP) % 360
    low, high = 0.0, 1.0
    l = INITIAL_LIGHTNESS

    # Бинарный поиск светлоты для целевой яркости
    for _ in range(10):
        r, g, b = _hsl_to_rgb(hue, INITIAL_SATURATION, l)
        current_brightness = 0.2126 * r + 0.7152 * g + 0.0722 * b

        if abs(current_brightness - TARGET_BRIGHTNESS) < 1:
            break

        if current_brightness < TARGET_BRIGHTNESS:
            low = l
        else:
            high = l
        l = (low + high) / 2

    return Color(r, g, b)
