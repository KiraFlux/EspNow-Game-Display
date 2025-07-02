from dataclasses import dataclass

import dearpygui.dearpygui as dpg

from dpg_ui.abc.widget import Widget
from dpg_ui.core.dpg.container import DpgContainer


@dataclass
class TabBar(DpgContainer):
    _reorderable: bool = False
    """Поддерживает перемещение вкладок"""

    def register(self, parent: Widget) -> None:
        self._onRegister(dpg.add_tab_bar(
            parent=parent.tag(),
            reorderable=self._reorderable
        ))


@dataclass
class Tab(DpgContainer):
    _label: str
    """Наименование вкладки"""

    _closable: bool = False
    """Вкладка может быть закрыта"""

    def register(self, parent: Widget) -> None:
        self._onRegister(dpg.add_tab(
            parent=parent.tag(),
            label=self._label,
            closable=self._closable,
        ))
