from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import field
from typing import MutableSequence
from typing import Self
from typing import final

from dpg_ui.abc.entities import Container
from dpg_ui.core.dpg.item import DpgTag
from dpg_ui.core.dpg.widget import DpgWidget


@dataclass
class DpgContainer[T](DpgWidget, Container[T], ABC):
    """Контейнер из DPG"""

    _items: MutableSequence[T] = field(init=False, default_factory=list)

    @abstractmethod
    def _registerItem(self, item: T) -> None:
        """Регистрация элемента в контейнере"""

    @final
    def add(self, item: T) -> Self:
        self._items.append(item)

        if self.isRegistered():
            self._registerItem(item)

        return self

    def _onRegister(self, tag: DpgTag) -> None:
        super()._onRegister(tag)

        self._updateVisibility()

        for item in self._items:
            self._registerItem(item)
