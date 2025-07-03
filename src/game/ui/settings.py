from dpg_ui.core.custom import CustomWidget
from dpg_ui.impl.container.window import ChildWindow
from game.core.environment import Environment


class SettingsPanel(CustomWidget):
    """Панель настроек"""

    def __init__(self, env: Environment) -> None:
        base = ChildWindow()
        super().__init__(base)
