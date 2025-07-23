from dpg_ui.core.custom import CustomWidget
from dpg_ui.impl.buttons import Button
from dpg_ui.impl.containers import VBox
from dpg_ui.impl.misc import Separator
from dpg_ui.impl.misc import Spacer
from dpg_ui.impl.text import Text
from game.core.environment import Environment
from game.res import Assets


class GameControlPanel(CustomWidget):
    """Панель управления игрой"""

    def __init__(self, env: Environment):
        super().__init__(
            VBox()
            .withFont(Assets.label_font)
            .add(
                Text("Панель управления")
            )
            .add(Spacer().withHeight(40))
            .add(Separator())

            .add(
                Button()
                .withWidth(-1)
                .withLabel("Сбросить доску")
                .withHandler(env.board.reset)
            )

            .add(
                Button()
                .withWidth(-1)
                .withLabel("Сбросить очки игроков")
            )

        )
