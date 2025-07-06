from itertools import product
from typing import Final

from dpg_ui.core.custom import CustomWidget
from dpg_ui.core.dpg.draw import DpgCanvas
from dpg_ui.core.dpg.draw import Rectangle
from dpg_ui.impl.containers import ChildWindow
from game.core.entities.board import Board
from game.core.entities.player import Player
from rs.lina.vector import Vector2D
from rs.misc.color import Color
from rs.misc.log import Logger

type Pos = Vector2D[int]


class BoardView(CustomWidget):
    """Визуализация игрового поля"""

    def __init__(self, board: Board, empty_cell_color: Color) -> None:
        self._empty_cell_border_color: Final = empty_cell_color
        self._log = Logger("game-board-view")

        board.size_subject.addObserver(self._onBoardResized)
        board.move_subject.addObserver(lambda args: self._onPlayerMove(*args))

        self._canvas = DpgCanvas(2000, 2000)

        base = ChildWindow(
            scrollable_y=True,
            scrollable_x=True
        ).add(self._canvas)

        super().__init__(base)

        self._grid = dict[Pos, Rectangle]()
        self._onBoardResized(board.size)

    def _createCellFigure(self, pos: Pos) -> Rectangle:
        cell_size = 100
        contour_thickness = cell_size // 10
        rounding = cell_size / 4

        pos_1 = pos * cell_size
        pos_2 = pos_1 + cell_size

        rectangle = Rectangle(
            _position_1=pos_1 + contour_thickness,
            _position_2=pos_2 - contour_thickness,
            _contour_thickness=contour_thickness,
            _fill_color=Color.none(),
            _contour_color=self._empty_cell_border_color,
            _rounding=rounding
        )

        return rectangle

    def _onBoardResized(self, board_size: Vector2D[int]) -> None:
        for pos, rectangle in self._grid.items():
            if not (0 <= pos.x < board_size.x and 0 <= pos.y < board_size.y):
                rectangle.hide()

        positions = map(
            lambda coords: Vector2D(*coords),
            product(range(board_size.x), range(board_size.y))
        )

        for pos in positions:

            if pos in self._grid:
                rectangle = self._grid[pos]

            else:
                rectangle = self._createCellFigure(pos)
                self._grid[pos] = rectangle
                self._canvas.add(rectangle)

            rectangle.show()

        self._log.write(f"Доска перестроена: {board_size}")

    def _onPlayerMove(self, player: Player, position: Vector2D[int]):

        rectangle = self._grid[position]
        rectangle.fill_color = player.team.color
        rectangle.contour_color = player.team.color.darker(0.4)

        self._log.write(f"Отображен ход игрока '{player}' на позиции {position}")
