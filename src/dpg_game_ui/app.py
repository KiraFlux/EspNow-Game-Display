from pathlib import Path
from typing import ClassVar
from typing import Final

from dpg_ui.core.app import App
from dpg_ui.core.dpg.font import DpgFont
from dpg_ui.impl.boxes.text import TextDisplay
from dpg_ui.impl.container.tab import Tab
from dpg_ui.impl.container.tab import TabBar
from dpg_ui.impl.container.window import ChildWindow
from dpg_ui.impl.container.window import Window
from dpg_ui.impl.text import Text
from game.core.environment import Environment
from rs.color import Color


class GameApp(App):
    _res: ClassVar = Path("res")
    _fonts: ClassVar = _res / "fonts"

    default_font: ClassVar = DpgFont(_fonts / r"JetBrainsMono.ttf", 20)
    label_font: ClassVar = DpgFont(_fonts / r"JetBrainsMono.ttf", 40)
    title_font: ClassVar = DpgFont(_fonts / r"SuperBrigadeHalftone-Jpax7.otf", 120)

    def __init__(self, env: Environment) -> None:
        super().__init__(Window("").withFont(self.default_font))
        self.env: Final = env

        pre_game_tab = (
            Tab("Начало")
            .add(
                ChildWindow(
                    height=200,
                    resizable_y=True,
                    # width=-1,
                    scrollable_y=True
                )
                .add(Text(_value_default="Sigma 3000 GAME", _color=Color.gray(0.8)).withFont(self.title_font))
            )
            .add(TextDisplay("Хост", default="00-11-22-33-44-55").withFont(self.label_font))
        )

        game_tab = Tab("Игра")

        logs_tab = Tab("Журнал")

        self.window.add(
            TabBar()
            .add(pre_game_tab)
            .add(game_tab)
            .add(logs_tab)
        )
