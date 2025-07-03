from __future__ import annotations

from abc import ABC
from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import field
from typing import MutableSequence
from typing import Optional
from typing import final

import dearpygui.dearpygui as dpg

from dpg_ui.abc.widget import Widget
from dpg_ui.core.dpg.tag import DpgTag
from dpg_ui.core.dpg.widget import DpgWidget
from lina.vector import Vector2D
from rs.color import Color


@dataclass
class DpgFigure(ABC):
    """Фигура из списка рисования"""

    __tag: Optional[DpgTag] = field(init=False, default=None)

    @final
    def register(self, canvas: DrawList) -> None:
        """Регистрация фигуры"""
        if self.__tag is not None:
            raise ValueError

        self.__tag = self._createTag(canvas.tag())

    @abstractmethod
    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        """Создать объект и получить тег"""


@dataclass
class DrawList(DpgWidget):
    """Список рисования"""

    width: int
    height: int

    _figures: MutableSequence[DpgFigure] = field(init=False, default_factory=list)

    def register(self, parent: Widget) -> None:
        self._onRegister(dpg.add_drawlist(
            parent=parent.tag(),
            width=self.width,
            height=self.height,
        ))

        for f in self._figures:
            f.register(self)

    def add(self, f: DpgFigure) -> DpgFigure:
        """Добавить фигуру на холст"""
        self._figures.append(f)

        if self.isRegistered():
            f.register(self)

        return f


@dataclass
class _HasBasicColor:
    color: Color = field(kw_only=True, default=Color.white())
    """Цвет"""


@dataclass
class _HasBorderThickness:
    border_thickness: float = field(kw_only=True, default=1.0)
    """Толщина контура"""


@dataclass
class _CommonFigureOptions:
    fill_color: Color = field(kw_only=True, default=Color.none())
    """Цвет заливки фигуры"""

    border_color: Color = field(kw_only=True, default=Color.white())
    """Цвет контура"""


@dataclass
class Rectangle(DpgFigure, _CommonFigureOptions, _HasBorderThickness):
    """Прямоугольник"""

    min_pos: Vector2D[float]
    """Меньшая вершина"""

    max_pos: Vector2D[float]
    """Большая вершина"""

    rounding: float = field(kw_only=True, default=0)
    """Скругление в пикселях"""

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.draw_rectangle(
            parent=parent_tag,

            color=self.border_color.toRGBA8888(),
            fill=self.fill_color.toRGBA8888(),
            thickness=self.border_thickness,

            rounding=self.rounding,
            pmin=self.min_pos.toTuple(),
            pmax=self.max_pos.toTuple(),
        )


@dataclass
class Circle(DpgFigure, _CommonFigureOptions, _HasBorderThickness):
    """Окружность"""

    center: Vector2D[float]
    """Центр"""

    radius: float
    """Радиус"""

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.draw_circle(
            parent=parent_tag,

            color=self.border_color.toRGBA8888(),
            fill=self.fill_color.toRGBA8888(),
            thickness=self.border_thickness,

            center=self.center.toTuple(),
            radius=self.radius,
        )


@dataclass
class Line(DpgFigure, _HasBasicColor, _HasBorderThickness):
    """Линия"""

    p1: Vector2D[float]
    """Первая вершина"""

    p2: Vector2D[float]
    """Вторая вершина"""

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.draw_line(
            parent=parent_tag,

            p1=self.p1.toTuple(),
            p2=self.p2.toTuple(),

            color=self.color.toRGBA8888(),
            thickness=self.border_thickness
        )


@dataclass
class TextFigure(DpgFigure, _HasBasicColor):
    """Нарисованный текст"""

    pos: Vector2D[float]
    """Позиция"""

    text: str
    """Текст"""

    size: int = field(kw_only=True, default=10)
    """Размер"""

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.draw_text(
            parent=parent_tag,

            pos=self.pos.toTuple(),
            text=self.text,
            size=self.size,
            color=self.color.toRGBA8888(),
        )
