from dpg_ui.core.custom import CustomWidget
from dpg_ui.impl.container.window import ChildWindow


class SettingsPanel(CustomWidget):
    """Панель настроек"""

    def __init__(self) -> None:
        base = ChildWindow()
        super().__init__(base)
