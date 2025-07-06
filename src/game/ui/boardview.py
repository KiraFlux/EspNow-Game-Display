from itertools import product
from typing import Final

from dpg_ui.core.custom import CustomWidget
from dpg_ui.core.dpg.draw import DpgCanvas
from dpg_ui.core.dpg.draw import Rectangle
from dpg_ui.impl.containers import ChildWindow
from dpg_ui.impl.containers import HBox
from dpg_ui.impl.sliders import FloatSlider
from game.core.entities.board import Board
from game.core.entities.player import Player
from game.ui.input2d import InputInt2D
from rs.lina.vector import Vector2D
from rs.misc.color import Color
from rs.misc.log import Logger

type Pos = Vector2D[int]


class BoardView(CustomWidget):
    """Визуализация игрового поля"""

    def __init__(self, board: Board, empty_cell_color: Color) -> None:
        self._log = Logger("game-board-view")

        self._empty_cell_border_color: Final = empty_cell_color
        self._board: Final = board
        self._scale: int = 1

        board.size_subject.addObserver(self._onBoardResized)
        board.move_subject.addObserver(lambda args: self._onPlayerMove(*args))

        def _update_board_size(new_size: Vector2D):
            board.size = new_size

        self._canvas = DpgCanvas(2000, 2000)

        self._canvas_window = (
            ChildWindow(
                scrollable_y=True,
                scrollable_x=True
            )
            .add(self._canvas)
        )

        _scale_slider = (
            FloatSlider("Масштаб", default=self._scale, interval=(0.1, 2.0), digits=2)
            .withHandler(self._onBoardRescaled)
            .withWidth(200)
        )

        base = (
            ChildWindow()
            .add(
                HBox()
                .add(_scale_slider)
                .add(
                    InputInt2D(
                        "Поле",
                        (1, 20),
                        on_change=_update_board_size,
                        default=board.size,
                    )
                )
            )
            .add(self._canvas_window)
        )

        super().__init__(base)

        self._grid = dict[Pos, Rectangle]()
        self._onBoardResized(board.size)

    def _calcCellSize(self) -> float:
        return 100
        # return min(
        #     self._canvas_window.getWidth() / self._board.size.x,
        #     self._canvas_window.getHeight() / self._board.size.y,
        # )

    def _applyCellTransform(self, pos: Vector2D, rect: Rectangle) -> None:
        """Применить и вернуть"""

        cell_size = self._calcCellSize() * self._scale

        thickness = cell_size // 10
        rect.position_1 = pos * cell_size + thickness
        rect.position_2 = pos * cell_size + cell_size - thickness
        rect.rounding = cell_size / 4
        rect.contour_thickness = thickness

    def _createCellFigure(self) -> Rectangle:

        rectangle = Rectangle(
            _fill_color=Color.none(),
            _contour_color=self._empty_cell_border_color,
        )

        return rectangle

    def _onBoardRescaled(self, scale: float) -> None:
        self._scale = scale

        for pos, rect in self._grid.items():
            self._applyCellTransform(pos, rect)

    def _onBoardResized(self, board_size: Vector2D[int]) -> None:
        for pos, rectangle in self._grid.items():
            if not (0 <= pos.x < board_size.x and 0 <= pos.y < board_size.y):
                rectangle.hide()

        positions = map(
            lambda coords: Vector2D(*coords),
            product(range(board_size.x), range(board_size.y))
        )

        i = 0
        for i, pos in enumerate(positions):

            if pos in self._grid:
                rectangle = self._grid[pos]

            else:
                rectangle = self._createCellFigure()
                self._applyCellTransform(pos, rectangle)
                self._grid[pos] = rectangle
                self._canvas.add(rectangle)

            rectangle.show()

        showed = i + 1
        total = len(self._grid)
        hidden = total - showed

        self._log.write(f"Доска перестроена: {board_size} | {total=}, {showed=}, {hidden=}")

    def _onPlayerMove(self, player: Player, position: Vector2D[int]):

        rectangle = self._grid[position]
        rectangle.fill_color = player.team.color
        rectangle.contour_color = player.team.color.darker(0.4)

        self._log.write(f"Отображен ход игрока '{player}' на позиции {position}")
