from typing import Final

from dpg_ui.core.app import App
from dpg_ui.impl.container.tab import Tab
from dpg_ui.impl.container.tab import TabBar
from dpg_ui.impl.container.window import Window
from game.core.environment import Environment


class GameApp(App):
    def __init__(self, env: Environment) -> None:
        super().__init__(Window(""))
        self.env: Final = env

        # логи
        # перед стартом (Адрес хоста, список игроков)
        # состояние игры (Игровая область, список игроков)

        self.window.add(
            TabBar()
            .add(Tab("Logs"))
            .add(Tab("Pre-game"))
            .add(Tab("Game"))
        )
