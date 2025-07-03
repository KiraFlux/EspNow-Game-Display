from dpg_ui.core.custom import CustomWidget
from dpg_ui.impl.container.window import ChildWindow
from game.core.entities.board import Board


class GameBoardView(CustomWidget):
    """Визуализация игрового поля"""

    def __init__(self, board: Board) -> None:
        base = ChildWindow()
        super().__init__(base)
