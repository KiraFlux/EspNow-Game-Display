from dpg_ui.core.custom import CustomWidget
from dpg_ui.impl.sliders import FloatSlider
from game.core.entities.rules import GameRules


class ControlPanel(CustomWidget):
    """Панель управления"""

    def __init__(self, rules: GameRules) -> None:
        base = (
            FloatSlider(
                "Кул-даун ходов",
                default=rules.move_cooldown_secs,
                units="сек",
                interval=(0, 10)
            ).withHandler(rules.setMoveCooldown)
        )

        super().__init__(base)
