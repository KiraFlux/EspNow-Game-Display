from dpg_ui.core.custom import CustomWidget
from dpg_ui.impl.sliders import FloatSlider
from game.core.environment import Environment


class ControlPanel(CustomWidget):
    """Панель управления"""

    def __init__(self, env: Environment) -> None:
        def _update_cooldown(v: float) -> None:
            env.rules.player_move_cooldown_secs = v

        base = (
            FloatSlider(
                "Кул-даун ходов",
                default=env.rules.player_move_cooldown_secs,
                on_change=_update_cooldown,
                units="сек",
                interval=(0, 10)
            )
        )

        super().__init__(base)
