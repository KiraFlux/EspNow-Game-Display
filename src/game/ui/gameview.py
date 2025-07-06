from dpg_ui.core.custom import CustomWidget
from dpg_ui.impl.boxes import DisplayText
from dpg_ui.impl.buttons import CheckBox
from dpg_ui.impl.containers import ChildWindow
from dpg_ui.impl.containers import HBox
from dpg_ui.impl.containers import Tab
from dpg_ui.impl.containers import TabBar
from dpg_ui.impl.containers import VBox
from dpg_ui.impl.misc import Spacer
from game.core.environment import Environment
from game.res import Assets
from game.ui.boardview import BoardView
from game.ui.playerlist import PlayerList
from game.ui.teamlist import TeamList


class GameView(CustomWidget):

    def __init__(self, env: Environment) -> None:
        host_mac_display = DisplayText("Хост", default="Ожидание...").withWidth(300)

        env.host_mac_subject.addObserver(host_mac_display.setValue)

        def _env_rules_moves_available(x):
            env.rules.moves_available = x

        base = (
            HBox()
            .add(
                ChildWindow(
                    _width=400,
                    resizable_x=True,
                    background=True
                )
                .add(
                    TabBar()
                    .add(
                        Tab("Игроки").add(PlayerList(env.player_registry))
                    )
                    .add(
                        Tab("Команды").add(TeamList(env.team_registry))
                    )
                )
            )
            .add(
                VBox()
                .add(
                    HBox()
                    .withFont(Assets.label_font)
                    .add(
                        CheckBox(_value=env.rules.moves_available)
                        .withLabel("Разрешить ходы")
                        .withHandler(_env_rules_moves_available)
                    )
                    .add(Spacer(width=200))
                    .add(host_mac_display)
                )
                .add(
                    BoardView(env.board, env.team_registry.default_team.color.darker(0.6))
                )
            )
        )

        super().__init__(base)
