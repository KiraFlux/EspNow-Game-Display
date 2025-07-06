from dataclasses import dataclass

from game.abc.valuegen import ValueGenerator
from rs.misc.color import Color


@dataclass(frozen=True, kw_only=True)
class ColorGenerator(ValueGenerator[Color]):
    """Генератор цвета"""

    hue: ValueGenerator[float]
    saturation: ValueGenerator[float]
    light: ValueGenerator[float]

    def calc(self, x: int) -> Color:
        return Color.fromHSL(
            self.hue.calc(x),
            self.saturation.calc(x),
            self.light.calc(x)
        )
