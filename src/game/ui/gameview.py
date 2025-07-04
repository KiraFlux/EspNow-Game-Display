from dpg_ui.core.custom import CustomWidget
from dpg_ui.impl.boxes import TextDisplay
from dpg_ui.impl.containers import ChildWindow
from dpg_ui.impl.containers import HBox
from dpg_ui.impl.containers import Tab
from dpg_ui.impl.containers import TabBar
from dpg_ui.impl.containers import VBox
from dpg_ui.impl.text import Text
from game.core.environment import Environment
from game.res import Assets
from game.ui.boardview import BoardView
from game.ui.playerlist import PlayerList
from game.ui.teamlist import TeamList
from rs.color import Color


class GameView(CustomWidget):

    def __init__(self, env: Environment) -> None:
        host_mac_display = TextDisplay("Хост", default="Ожидание...", width=300).withFont(Assets.label_font)

        env.host_mac_subject.addObserver(host_mac_display.setValue)

        base = (
            HBox()
            .add(
                ChildWindow(
                    width=400,
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
                    .add(host_mac_display)
                    .add(Text("GAME", color=Color.fromHex('#affff8')).withFont(Assets.title_font))
                )
                .add(
                    BoardView(env.board)
                )
            )
        )

        super().__init__(base)
