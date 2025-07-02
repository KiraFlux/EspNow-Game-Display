from dataclasses import dataclass
from typing import ClassVar
from typing import Final
from typing import Self


@dataclass(frozen=True)
class Color:
    """Цвет"""

    _rgba_8888_max: ClassVar = 255
    """Максимальное значение канала в формате RGB888"""

    _luma_r: ClassVar = 0.2126
    _luma_g: ClassVar = 0.7152
    _luma_b: ClassVar = 0.0722

    red: float
    """Компонента красного [0;1]"""
    green: float
    """Компонента зеленого [0;1]"""
    blue: float
    """Компонента синего [0;1]"""
    alpha: float
    """Компонента прозрачности [0;1]"""

    def __post_init__(self) -> None:
        assert 0.0 <= self.red <= 1.0
        assert 0.0 <= self.green <= 1.0
        assert 0.0 <= self.blue <= 1.0
        assert 0.0 <= self.alpha <= 1.0

    # from

    @classmethod
    def gray(cls, grayness: float) -> Self:
        """
        Создать серый
        :param grayness Значение серого [0;1]
        """
        return cls(grayness, grayness, grayness, 1.0)

    @classmethod
    def fromHex(cls, _hex: str) -> Self:
        """Создать цвет на основе HEX строки"""
        assert len(_hex) == 7
        assert _hex[0] == '#'

        r = int(_hex[1:3], 16)
        g = int(_hex[3:5], 16)
        b = int(_hex[5:7], 16)

        return cls.fromRGB888(r, g, b)

    @classmethod
    def fromRGB888(cls, r: int, g: int, b: int) -> Self:
        """Создать из формата RGB888"""
        return cls.fromRGBA8888(r, g, b, cls._rgba_8888_max)

    @classmethod
    def fromRGBA8888(cls, r: int, g: int, b: int, a: int) -> Self:
        """Создать из формата RGBA888"""
        return cls(
            r / cls._rgba_8888_max,
            g / cls._rgba_8888_max,
            b / cls._rgba_8888_max,
            a / cls._rgba_8888_max,
        )

    @classmethod
    def fromHSL(cls, hue: float, saturation: float, lightness: float) -> Self:
        """Создать из формата HSL
        :param hue: от 0 до 360
        :param saturation: [0;1]
        :param lightness:  [0;1]
        :return:
        """

        c = (1 - abs(2 * lightness - 1)) * saturation
        x = c * (1 - abs((hue / 60) % 2 - 1))
        m = lightness - c / 2

        index = int(hue // 60) % 6

        table = (
            (c, x, 0),
            (x, c, 0),
            (0, c, x),
            (0, x, c),
            (x, 0, c),
            (c, 0, x),
        )

        r, g, b = table[index]
        return cls(r + m, g + m, b + m)

    # to

    def toRGB888(self) -> tuple[int, int, int]:
        """Преобразовать в формат RGB888"""
        return (
            int(self.red * self._rgba_8888_max),
            int(self.green * self._rgba_8888_max),
            int(self.blue * self._rgba_8888_max)
        )

    def toRGBA8888(self) -> tuple[int, int, int, int]:
        """Преобразовать в формат RGBA8888"""
        return (
            int(self.red * self._rgba_8888_max),
            int(self.green * self._rgba_8888_max),
            int(self.blue * self._rgba_8888_max),
            int(self.alpha * self._rgba_8888_max)
        )

    def toHex(self) -> str:
        """Преобразовать в HEX представление"""
        r, g, b = self.toRGB888()
        return f"#{r:02x}{g:02x}{b:02x}"

    # methods

    def brightness(self) -> float:
        """Вычислить нормализованную яркость"""
        return self._luma_r * self.red + self._luma_g * self.green + self._luma_b * self.blue


class Palette:
    """Палитра цветов"""

    white: Final = Color.fromHex("#ffffff")
    """Белый"""
    black: Final = Color.fromHex("#000000")
    """Черный"""
