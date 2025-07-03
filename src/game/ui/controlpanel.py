from dpg_ui.core.custom import CustomWidget
from dpg_ui.impl.boxes import IntInput
from dpg_ui.impl.container.detail import Detail
from dpg_ui.impl.container.window import ChildWindow
from game.core.environment import Environment


class ControlPanel(CustomWidget):
    """Панель управления"""

    def __init__(self, env: Environment) -> None:
        base = (
            ChildWindow()
            .add(
                Detail("Настройки игры")
                # .add(IntInput())
            )
        )

        super().__init__(base)
