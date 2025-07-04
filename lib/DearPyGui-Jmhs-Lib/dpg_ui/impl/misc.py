from dataclasses import dataclass
from typing import final

import dearpygui.dearpygui as dpg

from dpg_ui.core.dpg.item import DpgTag
from dpg_ui.core.dpg.widget import DpgWidget


@final
class Separator(DpgWidget):
    """Dpg: separator"""

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_separator(
            parent=parent_tag,
        )


@final
@dataclass(kw_only=True)
class Spacer(DpgWidget):
    """Dpg spacer"""

    width: int = 0
    height: int = 0

    def _createTag(self, parent_tag: DpgTag) -> DpgTag:
        return dpg.add_spacer(
            parent=parent_tag,
            width=self.width,
            height=self.height,
        )
