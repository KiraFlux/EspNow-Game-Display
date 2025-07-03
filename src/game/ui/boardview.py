from dpg_ui.core.custom import CustomWidget
from dpg_ui.core.dpg.draw import Circle
from dpg_ui.core.dpg.draw import DrawList
from dpg_ui.core.dpg.draw import Rectangle
from dpg_ui.impl.container.window import ChildWindow
from game.core.entities.board import Board
from game.core.entities.player import Player
from lina.vector import Vector2D
from misc.log import Logger


class BoardView(CustomWidget):
    """Визуализация игрового поля"""

    def __init__(self, board: Board) -> None:
        self._log = Logger("game-board-view")

        board.size_subject.addObserver(self._onBoardResized)
        board.move_subject.addObserver(lambda args: self._onPlayerMove(*args))

        self._canvas = DrawList(800, 800)
        self._canvas.add(Rectangle(Vector2D(0, 0), Vector2D(300, 300), rounding=50, border_thickness=10))
        self._canvas.add(Circle(Vector2D(300, 300), 200, border_thickness=10))

        base = ChildWindow().add(self._canvas)
        super().__init__(base)

    def _onBoardResized(self, new_size: Vector2D[int]) -> None:
        self._log.write(f"Доска перестроена: {new_size}")

    def _onPlayerMove(self, player: Player, position: Vector2D[int]):
        self._log.write(f"Отображен ход игрока '{player}' на позиции {position}")
