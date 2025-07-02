from abc import ABC
from dataclasses import dataclass
from dataclasses import field
from typing import MutableSequence
from typing import Self

from dpg_ui.abc.container import Container
from dpg_ui.abc.widget import Widget
from dpg_ui.core.dpg.item import DpgTag
from dpg_ui.core.dpg.item import DpgWidget


@dataclass
class DpgContainer(DpgWidget, Container, ABC):
    """Контейнер из DPG"""

    _items: MutableSequence[Widget] = field(init=False, default_factory=list)

    def add(self, item: Widget) -> Self:
        self._items.append(item)

        if self.isRegistered():
            item.register(self)

        return self

    def _onRegister(self, tag: DpgTag) -> None:
        super()._onRegister(tag)
        for item in self._items:
            item.register(self)
