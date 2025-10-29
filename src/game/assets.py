import os
from pathlib import Path
from typing import Final
from typing import final

from dpg_ui.core.dpg.font import DpgFont


@final
class Assets:
    """Игровые ресурсы"""

    # paths

    app_path: Final = Path(os.getcwd())

    resources_path: Final = app_path / "res"

    fonts_path: Final = resources_path / "fonts"

    # fonts

    default_font: Final = DpgFont(fonts_path / r"JetBrainsMono.ttf", 20)

    log_font: Final = default_font.sub(size=16)

    label_font: Final = default_font.sub(size=32)

    title_font: Final = DpgFont(fonts_path / r"Library3am-5V3Z.otf", 48)

    def __new__(cls):
        raise TypeError
