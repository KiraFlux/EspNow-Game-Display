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
class _Options:
    fill_color: Color = field(kw_only=True, default=Color.none())
    """Цвет заливки фигуры"""

    border_color: Color = field(kw_only=True, default=Color.white())
    """Цвет контура"""

    border_thickness: float = field(kw_only=True, default=1.0)
    """Толщина контура"""


@dataclass
class Rectangle(DpgFigure, _Options):
    """Прямоугольник"""

    p1: Vector2D[float]
    p2: Vector2D[float]

    rounding: float = field(kw_only=True, default=0)
    """Скругление в пикселях"""

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.draw_rectangle(
            parent=parent_tag,

            color=self.border_color.toRGBA8888(),
            fill=self.fill_color.toRGBA8888(),
            thickness=self.border_thickness,

            rounding=self.rounding,
            pmin=self.p1.toTuple(),
            pmax=self.p2.toTuple(),
        )


@dataclass
class Circle(DpgFigure, _Options):
    """Окружность"""

    center: Vector2D[float]
    radius: float

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
class TextFigure(DpgFigure):
    """Нарисованный текст"""

    pos: Vector2D[float]
    text: str

    size: int = field(kw_only=True, default=10)
    color: Color = field(kw_only=True, default=Color.white())

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.draw_text(
            parent=parent_tag,

            pos=self.pos.toTuple(),
            text=self.text,
            size=self.size,
            color=self.color.toRGBA8888(),
        )
