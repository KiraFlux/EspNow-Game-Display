from dataclasses import dataclass

import dearpygui.dearpygui as dpg

from dpg_ui.abc.widget import Widget
from dpg_ui.core.dpg.container import DpgContainer


@dataclass
class Detail(DpgContainer):
    """Сворачивающийся заголовок"""

    _label: str
    """Заголовок"""
    _default_open: bool = False
    """Открыт по умолчанию"""

    def register(self, parent: Widget) -> None:
        self._onRegister(dpg.add_collapsing_header(
            parent=parent.tag(),
            label=self._label,
            default_open=self._default_open,
        ))
