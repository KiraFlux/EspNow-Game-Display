from dataclasses import dataclass

from game.abc.valuegen import ValueGenerator


@dataclass(frozen=True, kw_only=True)
class LoopStepGenerator(ValueGenerator[float]):
    """Закольцованный шагающий генератор"""

    start: float
    """Начальное значение"""
    step: float
    """Шаг"""
    loop: float
    """Модуль"""

    def calc(self, x: int) -> float:
        return (self.start + x * self.step) % self.loop
