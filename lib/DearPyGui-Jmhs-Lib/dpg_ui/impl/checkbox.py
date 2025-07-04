from dataclasses import dataclass
from typing import Callable
from typing import final

import dearpygui.dearpygui as dpg

from dpg_ui.core.dpg.item import DpgTag
from dpg_ui.core.dpg.traits import DpgValued
from dpg_ui.core.dpg.widget import DpgWidget


@final
@dataclass
class CheckBox(DpgWidget, DpgValued[bool]):
    """Dpg: checkbox"""

    _label: str

    _on_change: Callable[[bool], None] = None

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_checkbox(
            parent=parent_tag,
            label=self._label,
            default_value=bool(self._value_default),
            callback=None if self._on_change is None else (lambda _: self._on_change(self.getValue()))
        )
