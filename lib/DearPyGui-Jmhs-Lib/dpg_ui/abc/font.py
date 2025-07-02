from abc import ABC
from abc import abstractmethod

from dpg_ui.abc.item import Item


class Font[T](Item[T], ABC):
    """Шрифт"""

    @abstractmethod
    def _register(self) -> None:
        """Зарегистрировать шрифт"""
