from dpg_ui.core.app import App
from dpg_ui.impl.containers import Tab
from dpg_ui.impl.containers import TabBar
from dpg_ui.impl.containers import Window
from game.core.environment import Environment
from game.res import Assets
from game.ui.gamecontrol import GameControlPanel
from game.ui.gameview import GameView
from game.ui.logview import LogView


class GameApp(App):

    def __init__(self, env: Environment) -> None:
        super().__init__(Window().withFont(Assets.default_font))

        self.window.add(
            TabBar()
            .add(Tab("Игра").add(GameView(env)))
            .add(Tab("Управление").add(GameControlPanel(env)))
            .add(Tab("Журнал").add(LogView()))
        )
