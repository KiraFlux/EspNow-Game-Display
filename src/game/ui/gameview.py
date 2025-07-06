from dpg_ui.core.custom import CustomWidget
from dpg_ui.impl.boxes import DisplayText
from dpg_ui.impl.containers import ChildWindow
from dpg_ui.impl.containers import HBox
from dpg_ui.impl.containers import Tab
from dpg_ui.impl.containers import TabBar
from dpg_ui.impl.containers import VBox
from dpg_ui.impl.misc import Spacer
from game.core.environment import Environment
from game.res import Assets
from game.ui.boardview import BoardView
from game.ui.input2d import InputInt2D
from game.ui.playerlist import PlayerList
from game.ui.teamlist import TeamList
from lina.vector import Vector2D


class GameView(CustomWidget):

    def __init__(self, env: Environment) -> None:
        host_mac_display = DisplayText("Хост", default="Ожидание...").withWidth(300)

        env.host_mac_subject.addObserver(host_mac_display.setValue)

        def _update_board_size(new_size: Vector2D):
            env.board.size = new_size

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
                    .add(
                        InputInt2D(
                            "Поле",
                            (1, 20),
                            on_change=_update_board_size,
                            default=env.board.size,
                        )
                    )
                    .add(Spacer(width=300))
                    .add(host_mac_display)
                ).withFont(Assets.label_font)
                .add(
                    BoardView(env.board)
                )
            )
        )

        super().__init__(base)
