from dataclasses import dataclass
from typing import Final, Self
from functools import cache
import math


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
HUE_START = 15  # Начальный оттенок (теплый оранжевый)
HUE_STEP = 360 / GOLDEN_RATIO  # Шаг оттенка (~222.5°)
SAT_AMPLITUDE = 0.15  # Размах насыщенности
SAT_BASE = 0.6  # Базовая насыщенность
LIGHT_AMPLITUDE = 0.1  # Размах яркости
LIGHT_BASE = 0.8  # Базовая яркость


def _hsl_to_rgb(h: float, s: float, l: float) -> tuple[int, int, int]:
    """Преобразование HSL в RGB (0≤h<360, 0≤s≤1, 0≤l≤1)"""
    c = (1 - abs(2 * l - 1)) * s
    x = c * (1 - abs((h / 60) % 2 - 1))
    m = l - c / 2

    if 0 <= h < 60:
        r, g, b = c, x, 0
    elif 60 <= h < 120:
        r, g, b = x, c, 0
    elif 120 <= h < 180:
        r, g, b = 0, c, x
    elif 180 <= h < 240:
        r, g, b = 0, x, c
    elif 240 <= h < 300:
        r, g, b = x, 0, c
    else:
        r, g, b = c, 0, x

    r = round((r + m) * 255)
    g = round((g + m) * 255)
    b = round((b + m) * 255)
    return r, g, b


@cache
def get_team_color(team: int) -> Color:
    """Генерация уникального цвета для команды"""
    # Основной оттенок (золотое сечение)
    hue = (HUE_START + (team - 1) * HUE_STEP) % 360

    # Вариации насыщенности и яркости с разными фазами
    sat_phase = (team * 0.618) % (2 * math.pi)
    light_phase = (team * 1.618) % (2 * math.pi)

    # Синусоидальные колебания параметров
    saturation = SAT_BASE + SAT_AMPLITUDE * math.sin(sat_phase)
    lightness = LIGHT_BASE + LIGHT_AMPLITUDE * math.sin(light_phase)

    # Ограничение диапазонов
    saturation = max(0.5, min(0.7, saturation))
    lightness = max(0.75, min(0.85, lightness))

    r, g, b = _hsl_to_rgb(hue, saturation, lightness)
    return Color(r, g, b)