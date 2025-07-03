from dpg_ui.core.app import App
from dpg_ui.impl.boxes import TextDisplay
from dpg_ui.impl.container.box import HBox
from dpg_ui.impl.container.box import VBox
from dpg_ui.impl.container.tab import Tab
from dpg_ui.impl.container.tab import TabBar
from dpg_ui.impl.container.window import Window
from dpg_ui.impl.text import Text
from game.core.environment import Environment
from game.res import Assets
from game.ui.gameboard import GameBoardView
from game.ui.logview import LogView
from game.ui.player import PlayerList
from game.ui.settings import SettingsPanel
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
                        .add(Text(_value_default="Sigma 3000 GAME", _color=Color.fromHex('#ffaa88')).withFont(Assets.title_font))
                    )

                    .add(
                        GameBoardView(env.board)
                    )
                )
            )
        )

        logs_tab = (
            Tab("Журнал")
            .add(LogView())
        )

        settings_tab = (
            Tab("Настройки")
            .add(SettingsPanel(env))
        )

        self.window.add(
            TabBar()
            .add(game_tab)
            .add(logs_tab)
            .add(settings_tab)
        )
