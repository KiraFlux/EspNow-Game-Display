from itertools import product
from typing import Dict
from typing import Final
from typing import Mapping
from typing import Optional
from typing import Set
from typing import Tuple

from kf_dpg.core.custom import CustomWidget
from kf_dpg.core.dpg.draw import DpgCanvas
from kf_dpg.core.dpg.draw import Rectangle
from kf_dpg.impl.buttons import Button
from kf_dpg.impl.containers import ChildWindow
from kf_dpg.impl.containers import HBox
from kf_dpg.impl.containers import VBox
from kf_dpg.impl.misc import Spacer
from kf_dpg.impl.sliders import FloatSlider
from game.core.entities.board import Board
from game.core.entities.board import Cell
from game.core.entities.player import Player
from game.core.entities.player import Team
from rs.lina.vector import Vector2D
from rs.misc.color import Color
from rs.misc.log import Logger

type Pos = Vector2D[int]


class BoardView(CustomWidget):
    """Визуализация игрового поля с сохранением всех клеток и правильным управлением видимостью"""

    empty_cell_border_color: Final[Color] = Team.default().color.darker(0.58)

    base_thickness_ratio: Final[float] = 0.1
    base_rounding_ratio: Final[float] = 0.25
    default_scale: Final[float] = 1.0

    def __init__(self, board: Board) -> None:
        self._log = Logger("game-board-view")
        self._board = board
        self._scale: float = self.default_scale
        self._grid: Dict[Pos, Rectangle] = {}
        self._visible_cells: Set[Pos] = set()
        self._last_window_size: Optional[Tuple[int, int]] = None
        self._last_board_size: Vector2D[int] = board.size

        board.size_subject.addListener(self._handleBoardResize)
        board.move_subject.addListener(lambda args: self._handlePlayerMove(*args))
        board.update_subject.addListener(self._handleBoardUpdate)

        self._canvas = DpgCanvas(2000, 2000)
        self._canvas_window = ChildWindow(scrollable_y=True, scrollable_x=True).add(self._canvas)

        super().__init__(
            VBox()
            .add(
                HBox()
                .add(
                    Button()
                    .withLabel("Обновить")
                    .withHandler(board.notifyUpdate)
                )
                .add(
                    Spacer()
                    .withWidth(50)
                )
                .add(
                    FloatSlider(
                        "Масштаб",
                        default=self._scale,
                        interval=(0.1, 2.0),
                        digits=2
                    )
                    .withHandler(self._handleScaleChange)
                    .withWidth(200)
                )
            )
            .add(self._canvas_window)
        )

        self._initializeBoard()

    def _prepareColor(self, pos: Pos, source: Color) -> Color:
        x = (2 * pos.x + 3 * pos.y) % 6
        return source.darker(0.04 * x)

    def _initializeBoard(self) -> None:
        """Инициализирует доску при создании виджета"""
        self._createAllCells()
        self._updateVisibility(self._board.size)
        self._log.write(f"Доска инициализирована: {self._board.size}")

    def _createAllCells(self) -> None:
        """Создает все возможные клетки для максимального размера доски"""
        max_size = Board.max_size

        for x, y in product(range(max_size), range(max_size)):
            pos = Vector2D(x, y)
            if pos not in self._grid:
                rect = self._createCell(pos)
                rect.hide()  # Скрываем при создании
                self._grid[pos] = rect

        self._log.write(f"Создано клеток: {len(self._grid)}")

    def _createCell(self, pos: Pos) -> Rectangle:
        """Создает новую клетку с заданной позицией"""
        rect = Rectangle(
            _fill_color=Color.none(),
            _contour_color=self._prepareColor(pos, self.empty_cell_border_color)
        )
        self._applyCellStyle(pos, rect, self._board.getState().get(pos))
        self._applyCellTransform(pos, rect)
        self._canvas.add(rect)
        return rect

    def _calculateCellSize(self) -> float:
        """Рассчитывает размер клетки с учетом масштаба и размеров окна"""
        return 100 * self._scale

    def _applyCellStyle(self, pos: Pos, rect: Rectangle, cell: Optional[Cell] = None) -> None:
        """Применяет стиль клетки на основе её состояния"""

        if cell:
            team_color = cell.owner.team.color
            rect.fill_color = team_color
            contour = team_color.darker(0.4)

        else:
            rect.fill_color = Color.none()
            contour = self.empty_cell_border_color

        rect.contour_color = self._prepareColor(pos, contour)

    def _applyCellTransform(self, pos: Pos, rect: Rectangle) -> None:
        """Применяет позицию и размер к клетке"""
        cell_size = self._calculateCellSize()
        thickness = cell_size * self.base_thickness_ratio
        rounding = cell_size * self.base_rounding_ratio

        rect.position_1 = Vector2D(
            pos.x,
            pos.y
        ) * cell_size + thickness

        rect.position_2 = Vector2D(
            (pos.x + 1),
            (pos.y + 1)
        ) * cell_size - thickness

        rect.rounding = rounding
        rect.contour_thickness = thickness

    def _updateVisibility(self, board_size: Vector2D[int]) -> None:
        """Обновляет видимость клеток в соответствии с размером доски"""
        new_visible = set()

        # Скрываем все клетки, которые не входят в новую доску
        for pos in self._visible_cells:
            if pos.x >= board_size.x or pos.y >= board_size.y:
                if rect := self._grid.get(pos):
                    rect.hide()

        # Показываем клетки в пределах новой доски
        for x in range(board_size.x):
            for y in range(board_size.y):
                pos = Vector2D(x, y)
                new_visible.add(pos)

                if rect := self._grid.get(pos):
                    rect.show()

        self._visible_cells = new_visible
        self._last_board_size = board_size
        self._log.write(f"Обновлена видимость: видимых {len(new_visible)}")

    def _updateAllCells(self) -> None:
        """Обновляет все видимые клетки"""
        for pos in self._visible_cells:
            self._updateCell(pos)

    def _updateCell(self, pos: Pos) -> None:
        """Обновляет конкретную клетку с актуальным состоянием из доски"""
        if rect := self._grid.get(pos):
            # Всегда получаем актуальное состояние из доски
            cell_state = self._board.getState().get(pos)
            self._applyCellStyle(pos, rect, cell_state)
            self._applyCellTransform(pos, rect)

    def _handleScaleChange(self, scale: float) -> None:
        """Обработчик изменения масштаба"""
        self._scale = scale
        self._updateAllCells()
        self._log.write(f"Масштаб изменен: {scale}")

    def _handleBoardResize(self, board_size: Vector2D[int]) -> None:
        """Обработчик изменения размера доски"""
        self._updateVisibility(board_size)
        self._updateAllCells()
        self._log.write(f"Размер доски изменен: {board_size}")

    def _handlePlayerMove(self, player: Player, position: Vector2D[int]) -> None:
        """Обработчик хода игрока"""
        if position in self._visible_cells:
            self._updateCell(position)
            self._log.write(f"Отображен ход игрока '{player}' на позиции {position}")

    def _handleBoardUpdate(self, state: Mapping[Pos, Cell]) -> None:
        """Обработчик полного обновления доски (включая сброс)"""
        # Обновляем ВСЕ видимые клетки, независимо от содержимого события
        for pos in self._visible_cells:
            self._updateCell(pos)

        self._log.write("Полное обновление доски выполнено")
