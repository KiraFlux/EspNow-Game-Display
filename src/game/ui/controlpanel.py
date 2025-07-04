from dpg_ui.core.custom import CustomWidget
from dpg_ui.impl.containers import Tab
from dpg_ui.impl.containers import TabBar
from dpg_ui.impl.sliders import FloatSlider
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
                        (1, 20),
                        on_change=_update_board_size,
                        default=env.board.size,
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
                        default=env.rules.player_move_cooldown_secs,
                        on_change=_update_cooldown,
                        units="сек",
                        interval=(0, 10)
                    )
                )
            )
        )

        super().__init__(base)
