from typing import Any
from typing import Callable

from dpg_ui.core.custom import CustomWidget
from dpg_ui.impl.buttons import Button
from dpg_ui.impl.containers import VBox
from dpg_ui.impl.misc import Separator
from dpg_ui.impl.misc import Spacer
from dpg_ui.impl.text import Text
from game.core.entities.player import Player
from game.core.entities.player import Team
from game.core.environment import Environment
from game.res import Assets


class GameControlPanel(CustomWidget):
    """Панель управления игрой"""

    def __init__(self, env: Environment):
        def _forEachPlayer(f: Callable[[Player], Any]):
            for p in env.player_registry.getAll().values():
                f(p)

        super().__init__(
            VBox()
            .withFont(Assets.label_font)
            .add(
                Text("Панель управления")
            )
            .add(Spacer().withHeight(100))
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
                .withLabel("Сбросить значения игроков")
                .withHandler(lambda: _forEachPlayer(lambda p: p.reset()))
            )

            .add(
                Button()
                .withWidth(-1)
                .withLabel("Выгнать всех из команд")
                .withHandler(lambda: _forEachPlayer(lambda p: p.setTeam(Team.default())))
            )

        )
