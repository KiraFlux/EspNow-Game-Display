from __future__ import annotations

from tkinter import Canvas
from tkinter import Event
from tkinter import Misc

from color import get_team_color
from color import get_text_color
from game.core.entities import Board
from game.core.entities import Vector2D
from game.ui.font import FontFactory
from game.ui.theme import Theme


class GameBoardView(Canvas):
    """Виджет для отображения игрового поля"""

    def __init__(self, master: Misc, board: Board) -> None:
        super().__init__(
            master,
            bg=Theme.current().secondary_background,
            highlightthickness=0
        )
        self._board = board
        self.bind("<Configure>", self._on_resize)

    def update_board(self, board: Board) -> None:
        """Обновить игровое поле"""
        self._board = board
        self._draw_board()

    def _on_resize(self, e: Event) -> None:
        """Перерисовать поле при изменении размера"""
        self._draw_board()

    def _draw_board(self) -> None:
        """Отрисовать игровое поле"""
        self.delete("all")

        width = self.winfo_width()
        height = self.winfo_height()
        cx, cy = self._board.size.x, self._board.size.y

        if cx == 0 or cy == 0:
            return

        cell_size = min(width // cx, height // cy)
        offset_x = (width - cell_size * cx) // 2
        offset_y = (height - cell_size * cy) // 2

        # Отрисовка всех ячеек
        board_state = self._board.getState()
        for x in range(cx):
            for y in range(cy):
                pos = Vector2D(x, y)
                cell = board_state.get(pos)
                team = 0
                if cell is not None and cell.owner is not None:
                    team = cell.owner.team

                # Отрисовка ячейки
                x1 = offset_x + x * cell_size
                y1 = offset_y + y * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                color = get_team_color(team)
                self.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline=Theme.current().border,
                    width=1
                )

                if team > 0:
                    self.create_text(
                        (x1 + x2) // 2, (y1 + y2) // 2,
                        text=str(team),
                        fill=get_text_color(color),
                        font=FontFactory.heading()
                    )
