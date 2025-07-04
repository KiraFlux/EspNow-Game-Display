from typing import Callable
from typing import Final

from dpg_ui.abc.traits import Intervaled
from dpg_ui.abc.traits import Valued
from dpg_ui.core.custom import CustomWidget
from dpg_ui.impl.boxes import IntInput
from dpg_ui.impl.containers import VBox
from dpg_ui.impl.text import Text
from lina.vector import Vector2D


class InputInt2D(CustomWidget, Valued[Vector2D[int]], Intervaled[int]):
    """Окно ввода 2D вектора"""

    def __init__(
            self,
            label: str,
            interval: tuple[int, int],
            *,
            on_change: Callable[[Vector2D], None] = 0,
            default: Vector2D[int] = Vector2D(0, 0),
            label_x: str = "x",
            label_y: str = "y",
            width: int = 0,
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

        self._y = IntInput(
            label=label_y,
            on_change=_on_change_y,
            default=default.y,
            width=width,
            step=step,
            step_fast=step_fast,
            interval_max=interval_max,
            interval_min=interval_min,
        )

        self._x = IntInput(
            label=label_x,
            on_change=_on_change_x,
            default=default.x,
            width=width,
            step=step,
            step_fast=step_fast,
            interval_max=interval_max,
            interval_min=interval_min,
        )

        base = (
            VBox()
            .add(Text(label))
            .add(self._x)
            .add(self._y)
        )

        super().__init__(base)

    def _onIntervalMinChanged(self, new_min: int) -> None:
        self._x.setIntervalMin(new_min)
        self._y.setIntervalMin(new_min)

    def _onIntervalMaxChanged(self, new_max: int) -> None:
        self._x.setIntervalMax(new_max)
        self._y.setIntervalMax(new_max)

    def setValue(self, value: Vector2D[int]) -> None:
        self._x.setValue(value.x)
        self._y.setValue(value.y)
        self._on_change(value)

    def getValue(self) -> Vector2D[int]:
        return Vector2D(
            self._x.getValue(),
            self._y.getValue()
        )
