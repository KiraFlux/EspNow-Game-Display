from pathlib import Path
from typing import ClassVar
from typing import Final

from dpg_ui.core.app import App
from dpg_ui.core.dpg.font import DpgFont
from dpg_ui.impl.container.tab import Tab
from dpg_ui.impl.container.tab import TabBar
from dpg_ui.impl.container.window import Window
from dpg_ui.impl.display.text import DisplayText
from game.core.environment import Environment


class GameApp(App):
    _res: ClassVar = Path("res")
    _fonts: ClassVar = _res / "fonts"

    default_font: ClassVar = DpgFont(_fonts / r"JetBrainsMono.ttf", 20)
    title_font: ClassVar = DpgFont(_fonts / r"SuperBrigadeHalftone-Jpax7.otf", 80)

    def __init__(self, env: Environment) -> None:
        super().__init__(Window("").setFont(self.default_font))
        self.env: Final = env

        # логи
        # перед стартом (Адрес хоста, список игроков)
        # состояние игры (Игровая область, список игроков)

        pre_game_tab = (
            Tab("Начало")
            .add(DisplayText(_value_default="Sigma 3000 GAME").setFont(self.title_font))
        )

        self.window.add(
            TabBar()
            .add(pre_game_tab)
            .add(Tab("Игра"))
            .add(Tab("Журнал"))
        )
