from abc import ABC
from abc import abstractmethod
from typing import Optional
from typing import final


class Item[T](ABC):
    """Элемент системы"""

    @abstractmethod
    def tag(self) -> Optional[T]:
        """Получить тег элемента"""

    @final
    def isRegistered(self) -> bool:
        """Виджет уже зарегистрирован"""
        return self.tag() is not None
