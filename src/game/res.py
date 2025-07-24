from pathlib import Path

from dpg_ui.core.dpg.font import DpgFont


class Assets:
    """Игровые ресурсы"""

    # paths

    resources_path = Path(r"A:\Projects\EspNow-Game-Display\res")

    fonts_path = resources_path / "fonts"

    # fonts

    default_font = DpgFont(fonts_path / r"JetBrainsMono.ttf", 20)

    log_font = default_font.sub(size=16)

    label_font = default_font.sub(size=32)

    title_font = DpgFont(fonts_path / r"Library3am-5V3Z.otf", 48)

    def __new__(cls):
        raise TypeError
