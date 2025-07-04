from dataclasses import dataclass
from dataclasses import field
from typing import Callable
from typing import final

from dearpygui import dearpygui as dpg

from dpg_ui.core.dpg.item import DpgTag
from dpg_ui.core.dpg.widget import DpgWidget


@final
@dataclass
class Button(DpgWidget):
    """Dpg: button"""

    _label: str
    """Надпись"""

    _on_click: Callable[[], None] = None
    """Callback"""

    _small: bool = field(kw_only=True, default=False)
    """Меньший размер кнопки"""

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_button(
            label=self._label,
            parent=parent_tag,
            small=self._small,
            callback=None if self._on_click is None else (lambda _: self._on_click())
        )
