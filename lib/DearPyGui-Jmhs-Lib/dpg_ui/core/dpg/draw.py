from __future__ import annotations

from abc import ABC
from dataclasses import dataclass
from dataclasses import field
from typing import final

import dearpygui.dearpygui as dpg

from dpg_ui.abc.entities import Canvas
from dpg_ui.abc.entities import Figure
from dpg_ui.core.dpg.container import DpgContainer
from dpg_ui.core.dpg.item import DpgTag
from dpg_ui.core.dpg.traits import DpgVisibility
from lina.vector import Vector2D
from rs.color import Color


class _DpgFigure(DpgVisibility, Figure, ABC):
    """Фигура из списка рисования"""

    @final
    def register(self, canvas: Canvas[DpgTag]) -> None:
        self._onRegister(self._createTag(canvas.tag()))


@final
@dataclass
class DpgCanvas(Canvas[DpgTag], DpgContainer):
    """Список рисования"""

    width: int
    height: int

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_drawlist(
            parent=parent_tag,
            width=self.width,
            height=self.height,
        )

    def _registerItem(self, item: _DpgFigure) -> None:
        item.register(self)


@dataclass
class _HasFillColor:
    """Фигура поддерживает цвет заливки"""

    _fill_color: Color = field(kw_only=True, default=Color.white())
    """Цвет заливки фигуры"""


@dataclass
class _HasContourThickness:
    """Фигура поддерживает толщину контура"""

    _contour_thickness: float = field(kw_only=True, default=1.0)
    """Толщина контура"""


@dataclass
class _HasContourColor:
    """Фигура поддерживает цвет контура"""

    _contour_color: Color = field(kw_only=True, default=Color.white())
    """Цвет контура"""


@dataclass
class _HasTwoVertexes:
    """Фигура задаётся двумя координатами"""

    _position_1: Vector2D[float]
    """Первая координата"""

    _position_2: Vector2D[float]
    """Вторая координата"""


@final
@dataclass
class Rectangle(_DpgFigure, _HasTwoVertexes, _HasFillColor, _HasContourColor, _HasContourThickness):
    """Прямоугольник"""

    _rounding: float = field(kw_only=True, default=0)
    """Скругление в пикселях"""

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.draw_rectangle(
            parent=parent_tag,

            color=self._contour_color.toRGBA8888(),
            fill=self._fill_color.toRGBA8888(),
            thickness=self._contour_thickness,

            rounding=self._rounding,
            pmin=self._position_1.toTuple(),  # todo автоопределение меньшей вершины, если нужно
            pmax=self._position_2.toTuple(),
        )


@final
@dataclass
class Line(_DpgFigure, _HasTwoVertexes, _HasFillColor, _HasContourThickness):
    """Линия"""

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.draw_line(
            parent=parent_tag,

            p1=self._position_1.toTuple(),
            p2=self._position_2.toTuple(),

            color=self._fill_color.toRGBA8888(),
            thickness=self._contour_thickness
        )


@dataclass
class _HasSinglePosition:
    _position: Vector2D[float]
    """Позиция"""


@dataclass
class _HasSize:
    _size: float = field(kw_only=True)
    """Размер в пикселях"""


@final
@dataclass
class Circle(_DpgFigure, _HasSinglePosition, _HasSize, _HasContourColor, _HasContourThickness, _HasFillColor):
    """Окружность"""

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.draw_circle(
            parent=parent_tag,

            color=self._contour_color.toRGBA8888(),
            fill=self._fill_color.toRGBA8888(),
            thickness=self._contour_thickness,

            center=self._position.toTuple(),
            radius=self._size / 2,  # Диаметр
        )


@final
@dataclass
class TextFigure(_DpgFigure, _HasSinglePosition, _HasSize, _HasFillColor):
    """Нарисованный текст"""

    text: str
    """Текст"""

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.draw_text(
            parent=parent_tag,

            pos=self._position.toTuple(),
            text=self.text,
            size=self._size,

            color=self._fill_color.toRGBA8888(),
        )
