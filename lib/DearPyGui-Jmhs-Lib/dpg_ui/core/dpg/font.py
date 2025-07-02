from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import ClassVar
from typing import MutableSequence
from typing import Optional
from typing import final

import dearpygui.dearpygui as dpg

from dpg_ui.abc.font import Font
from dpg_ui.core.dpg.tag import DpgTag


@dataclass
class DpgFont(Font[DpgTag]):
    """Элемент DPG"""

    _fonts: ClassVar[MutableSequence[Font]] = list()
    """Загруженные шрифты"""

    _source: Path
    """Файл шрифта"""
    _size: int
    """Размер шрифта в пикселях"""
    _smooth: bool = True
    """Сглаживание шрифта"""
    _tag: Optional[DpgTag] = field(init=False, default=None)
    """Тег"""

    def __post_init__(self) -> None:
        self._fonts.append(self)

    @classmethod
    def load(cls) -> None:
        """Загрузить все шрифты"""
        with dpg.font_registry():
            for font in cls._fonts:
                font._register()

    @final
    def _register(self) -> None:
        self._tag = dpg.add_font(
            file=str(self._source),
            size=self._size,
            pixel_snapH=not self._smooth
        )

        dpg.add_font_range_hint(dpg.mvFontRangeHint_Default, parent=self._tag)
        dpg.add_font_range_hint(dpg.mvFontRangeHint_Cyrillic, parent=self._tag)

    @final
    def tag(self) -> Optional[DpgTag]:
        """Получить тег"""
        return self._tag
