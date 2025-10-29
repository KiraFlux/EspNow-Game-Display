from typing import Callable
from typing import Final

from kf_dpg.abc.traits import Intervaled
from kf_dpg.abc.traits import Valued
from kf_dpg.core.custom import CustomWidget
from kf_dpg.impl.boxes import IntInput
from kf_dpg.impl.containers import HBox
from kf_dpg.impl.containers import VBox
from kf_dpg.impl.text import Text
from rs.lina.vector import Vector2D


class Int2DInput(CustomWidget, Valued[Vector2D[int]], Intervaled[int]):
    """Окно ввода 2D вектора"""

    def __init__(
            self,
            label: str,
            interval: tuple[int, int],
            *,
            on_change: Callable[[Vector2D], None] = None,
            default: Vector2D[int] = Vector2D(0, 0),
            width: int = 500,
            step: int = 1,
            step_fast: int = 1
    ) -> None:

        self._on_change: Final = on_change

        if on_change is None:
            _on_change_x = None
            _on_change_y = None
        else:
            def _on_change_x(x):
                on_change(Vector2D(x, self._y.getValue()))

            def _on_change_y(y):
                on_change(Vector2D(self._x.getValue(), y))

        interval_min, interval_max = interval

        item_width = width // 3

        self._y = IntInput(
            default=default.y,
            step=step,
            step_fast=step_fast,
            interval_max=interval_max,
            interval_min=interval_min,
        ).withWidth(item_width).withHandler(_on_change_y)

        self._x = IntInput(
            default=default.x,
            step=step,
            step_fast=step_fast,
            interval_max=interval_max,
            interval_min=interval_min,
        ).withWidth(item_width).withHandler(_on_change_x)

        base = (
            HBox()
            .add(
                VBox()
                .add(self._x)
                .add(self._y)
            )
            .add(Text(label))
        )

        super().__init__(base)

    def getIntervalMax(self) -> int:
        return self._x.getIntervalMax()

    def getIntervalMin(self) -> int:
        return self._x.getIntervalMin()

    def setIntervalMax(self, new_max: int) -> None:
        self._x.setIntervalMax(new_max)
        self._y.setIntervalMax(new_max)

    def setIntervalMin(self, new_min: int) -> None:
        self._x.setIntervalMin(new_min)
        self._y.setIntervalMin(new_min)

    def setValue(self, value: Vector2D[int]) -> None:
        self._x.setValue(value.x)
        self._y.setValue(value.y)
        self._on_change(value)

    def getValue(self) -> Vector2D[int]:
        return Vector2D(
            self._x.getValue(),
            self._y.getValue()
        )
