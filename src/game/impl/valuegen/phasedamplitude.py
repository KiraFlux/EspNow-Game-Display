from dataclasses import dataclass
from math import sin

from game.abc.valuegen import ValueGenerator


@dataclass(frozen=True, kw_only=True)
class PhasedAmplitudeGenerator(ValueGenerator[float]):
    """Фазовый амплитудный генератор значений"""

    scale: float
    """Масштаб значения"""
    base: float
    """Базовое значение"""
    amplitude: float
    """Амплитуда значения"""

    def calc(self, x: int) -> float:
        return self.base + self.amplitude * sin(x * self.scale)
