from dataclasses import dataclass

import dearpygui.dearpygui as dpg

from dpg_ui.abc.widget import Widget
from dpg_ui.core.dpg.container import DpgContainer


@dataclass(kw_only=True)
class _Box(DpgContainer):
    _is_horizontal: bool

    def register(self, parent: Widget) -> None:
        self._onRegister(
            dpg.add_group(
                parent=parent.tag(),
                horizontal=self._is_horizontal
            )
        )


def VBox() -> _Box:
    """Вертикальный контейнер"""
    return _Box(_is_horizontal=False)


def HBox() -> _Box:
    """Горизонтальный контейнер"""
    return _Box(_is_horizontal=True)
