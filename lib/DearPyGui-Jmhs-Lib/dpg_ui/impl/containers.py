from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from typing import final

from dearpygui import dearpygui as dpg

from dpg_ui.abc.entities import Widget
from dpg_ui.core.dpg.container import DpgContainer
from dpg_ui.core.dpg.item import DpgTag
from dpg_ui.core.dpg.traits import DpgSizable
from dpg_ui.core.dpg.widget import DpgWidget


@dataclass
class _DpgWidgetContainer(DpgContainer[Widget[DpgWidget]], ABC):

    @final
    def _registerItem(self, item: Widget[DpgWidget]) -> None:
        item.register(self)


@dataclass
class _DpgSizableWidgetContainer(_DpgWidgetContainer, DpgSizable[int], ABC):

    def _onRegister(self, tag: DpgTag) -> None:
        super()._onRegister(tag)
        self._updateWidth()
        self._updateHeight()


@final
@dataclass(kw_only=True)
class _Box(_DpgSizableWidgetContainer):
    """Dpg: group"""

    _is_horizontal: bool

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_group(
            parent=parent_tag,
            horizontal=self._is_horizontal
        )


def VBox() -> _Box:
    """Вертикальный контейнер"""
    return _Box(_is_horizontal=False)


def HBox() -> _Box:
    """Горизонтальный контейнер"""
    return _Box(_is_horizontal=True)


@final
@dataclass
class Details(_DpgWidgetContainer):
    """Dpg: collapsing_header"""

    _label: str
    """Заголовок"""
    _default_open: bool = False
    """Открыт по умолчанию"""

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_collapsing_header(
            parent=parent_tag,
            label=self._label,
            default_open=self._default_open
        )


@final
@dataclass
class Tab(_DpgWidgetContainer):
    """Dpg: tab"""

    _label: str
    """Наименование вкладки"""

    _closable: bool = False
    """Вкладка может быть закрыта"""

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_tab(
            parent=parent_tag,
            label=self._label,
            closable=self._closable,
        )


@final
@dataclass
class TabBar(DpgContainer[Tab]):
    """Dpg: tab_bar"""

    _reorderable: bool = False
    """Поддерживает перемещение вкладок"""

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_tab_bar(
            parent=parent_tag,
            reorderable=self._reorderable
        )

    def _registerItem(self, item: Tab) -> None:
        item.register(self)


@final
@dataclass
class Window(_DpgSizableWidgetContainer):
    """Dpg: window"""

    _label: str
    """Заголовок окна"""

    _menubar: bool = False
    """Место под полосу меню"""

    _auto_size: bool = True
    """Размер окна автоматически подстраивается под виджеты"""

    # noinspection PyFinal
    def register(self, parent: Widget) -> None:
        self._onRegister(dpg.add_window(
            label=self._label,
            menubar=self._menubar,
            autosize=self._auto_size,
        ))

    def _createTag(self, parent_tag):
        raise RuntimeError


@final
@dataclass(kw_only=True)
class ChildWindow(_DpgSizableWidgetContainer):
    """Дочернее очно"""

    resizable_x: bool = False
    resizable_y: bool = False

    auto_size_x: bool = False
    auto_size_y: bool = False

    border: bool = True

    # Внешний вид
    background: bool = False
    menu_bar: bool = False
    scrollable_y: bool = True
    scrollable_x: bool = False

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_child_window(
            parent=parent_tag,
            border=self.border,
            frame_style=self.background,
            menubar=self.menu_bar,
            resizable_x=self.resizable_x,
            resizable_y=self.resizable_y,
            no_scrollbar=not self.scrollable_y,
            horizontal_scrollbar=self.scrollable_x,
            autosize_x=self.auto_size_x,
            autosize_y=self.auto_size_y,
        )
