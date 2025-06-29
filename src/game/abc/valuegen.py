from abc import ABC
from abc import abstractmethod


class ValueGenerator[T](ABC):
    """Генератор последовательности значений на основании входа"""

    @abstractmethod
    def calc(self, x: int) -> T:
        """Рассчитать значение"""
