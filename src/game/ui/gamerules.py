from dpg_ui.core.custom import CustomWidget
from dpg_ui.impl.boxes import IntInput
from dpg_ui.impl.containers import ComboBox
from dpg_ui.impl.containers import VBox
from dpg_ui.impl.misc import Separator
from dpg_ui.impl.misc import Spacer
from dpg_ui.impl.sliders import FloatSlider
from dpg_ui.impl.text import Text
from game.core.entities.rules import GameRules
from game.res import Assets
from rs.misc.color import Color


class GameRulesPanel(CustomWidget):
    """Панель управления игровым балансом"""

    def __init__(self, rules: GameRules) -> None:
        super().__init__(
            VBox()
            .withWidth(400)

            .add(
                Text("Баланс", color=Color.nitro())
                .withFont(Assets.label_font)
            )

            .add(Spacer().withHeight(40))
            .add(Separator())

            .add(
                FloatSlider(
                    "Кул-даун ходов",
                    default=rules.move_cooldown_secs,
                    units="сек",
                    interval=(0, 10)
                )
                .withHandler(rules.setMoveCooldown)
            )

            .add(Spacer().withHeight(20))
            .add(Separator())

            .add(
                Text("Очки за установку клетки", bullet=True)
            )
            .add(
                ComboBox(
                    _items_provider=rules.score.mode.getItems,
                    _value=rules.score.mode
                )
                .withLabel("Режим просмотра")
            )
            .add(
                IntInput(
                    rules.score.empty_cell,
                    step_fast=10,
                )
                .withLabel("Пусто")
                .withHandler(rules.score.setEmptyCell)
            )
            .add(
                IntInput(
                    rules.score.friend_cell,
                    step_fast=10,
                )
                .withLabel("Союзник")
                .withHandler(rules.score.setFriendCell)
            )
            .add(
                IntInput(
                    rules.score.enemy_cell,
                    step_fast=10,
                )
                .withLabel("Враг")
                .withHandler(rules.score.setEnemyCell)
            )
        )
