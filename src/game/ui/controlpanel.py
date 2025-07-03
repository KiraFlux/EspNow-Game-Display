from dpg_ui.core.custom import CustomWidget
from dpg_ui.impl.container.tab import Tab
from dpg_ui.impl.container.tab import TabBar
from dpg_ui.impl.slider.float_ import FloatSlider
from game.core.environment import Environment
from game.ui.input2d import InputInt2D
from lina.vector import Vector2D


class ControlPanel(CustomWidget):
    """Панель управления"""

    def __init__(self, env: Environment) -> None:
        def _update_board_size(new_size: Vector2D):
            env.board.size = new_size

        def _update_cooldown(v: float) -> None:
            env.rules.player_move_cooldown_secs = v

        base = (
            TabBar()
            .add(
                Tab("Настройки доски")
                .add(
                    InputInt2D(
                        "Размер доски",
                        _update_board_size,
                        default=env.board.size,
                        interval_min=1,
                        label_x="Ширина",
                        label_y="Высота",
                    )
                )
            )
            .add(
                Tab("Игровые правила")
                .add(
                    FloatSlider(
                        "Кул-даун ходов",
                        _update_cooldown,
                        _units="сек",
                        _interval_min=0.0,
                        _interval_max=10.0,
                        _value_default=env.rules.player_move_cooldown_secs
                    )
                )
            )
        )

        super().__init__(base)
