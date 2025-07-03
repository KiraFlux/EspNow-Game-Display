from dpg_ui.core.app import App
from dpg_ui.impl.boxes import TextDisplay
from dpg_ui.impl.button import Button
from dpg_ui.impl.container.box import HBox
from dpg_ui.impl.container.box import VBox
from dpg_ui.impl.container.tab import Tab
from dpg_ui.impl.container.tab import TabBar
from dpg_ui.impl.container.window import Window
from dpg_ui.impl.text import _Text
from game.core.environment import Environment
from game.res import Assets
from game.ui.controlpanel import ControlPanel
from game.ui.boardview import BoardView
from game.ui.logview import LogView
from game.ui.player import PlayerList
from rs.color import Color


class GameApp(App):

    def __init__(self, env: Environment) -> None:
        super().__init__(Window("").withFont(Assets.default_font))

        game_tab = (
            Tab("Игра")
            .add(
                HBox()
                .add(
                    PlayerList(env.player_registry)
                )
                .add(
                    VBox()
                    .add(
                        HBox()
                        .add(TextDisplay("Хост", default="00-11-22-33-44-55", width=300).withFont(Assets.label_font))
                        .add(_Text(_value_default="GAME", _color=Color.fromHex('#affff8')).withFont(Assets.title_font))
                    )
                    .add(
                        BoardView(env.board)
                    )
                )
            )
        )

        logs_tab = (
            Tab("Журнал")
            .add(LogView())
        )

        settings_tab = (
            Tab("Панель управления")
            .add(ControlPanel(env))
        )

        self.window.add(
            TabBar()
            .add(game_tab)
            .add(settings_tab)
            .add(logs_tab)
        )
