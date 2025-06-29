from __future__ import annotations

from tkinter import Canvas
from tkinter import Event
from tkinter import Misc
from typing import Optional

from game.core.entities import Board
from game.core.entities import Cell
from game.util import get_team_color
from lina.vector import Vector2D
from misc.color import Color
from misc.color import Palette
from ui.core.font import FontFactory
from ui.core.theme import Theme


class GameBoardView(Canvas):
    """Виджет для отображения игрового поля"""

    def __init__(self, master: Misc, board: Board) -> None:
        super().__init__(
            master,
            bg=Theme.current().secondary_background.toHex(),
            highlightthickness=0
        )
        self._board = board
        self.bind("<Configure>", self._on_resize)

    def update_board(self) -> None:
        """Обновить игровое поле"""
        self._draw_board()

    def _on_resize(self, e: Event) -> None:
        """Перерисовать поле при изменении размера"""
        self._draw_board()

    def _draw_board(self) -> None:
        """Отрисовать игровое поле"""
        self.delete("all")

        width = self.winfo_width()
        height = self.winfo_height()

        cell_size = min(width // self._board.size.x, height // self._board.size.y)

        offset = Vector2D(
            (width - cell_size * self._board.size.x) // 2,
            (height - cell_size * self._board.size.y) // 2
        )

        for x in range(self._board.size.x):
            for y in range(self._board.size.y):
                pos = Vector2D.new(x, y)

                cell = self._board.getState().get(pos)
                self._drawPlaceableCell(cell, cell_size, offset, pos)

    def _getCellColor(self, cell: Optional[Cell]) -> Color:
        if cell is None:
            return Theme.current().background

        return get_team_color(cell.owner.team)

    def _drawPlaceableCell(self, cell: Optional[Cell], cell_size: int, offset: Vector2D[int], origin: Vector2D[int]):
        cell_color = self._getCellColor(cell)

        a = origin * cell_size + offset
        b = a + Vector2D(cell_size, cell_size)

        self.create_rectangle(
            a.x, a.y, b.x, b.y,
            fill=cell_color.toHex(),
            outline=Theme.current().border.toHex(),
            width=1,
        )

        if cell is None:
            return

        text_pos = (a + b) / 2
        text_color = Palette.white if cell_color.brightness() < 0.9 else Palette.black

        self.create_text(
            text_pos.x, text_pos.y,
            text=str(cell.owner.team),
            fill=text_color.toHex(),
            font=FontFactory.heading()
        )
