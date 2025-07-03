from io import StringIO
from typing import Callable
from typing import Final

from dpg_ui.core.custom import CustomWidget
from dpg_ui.impl.container.window import ChildWindow
from dpg_ui.impl.text import Text
from misc.log import Logger


class TextIOEchoAdapter(StringIO):

    def __init__(self, on_write: Callable[[str], None]) -> None:
        super().__init__()
        self.on_write: Final = on_write

    def write(self, __s):
        self.on_write(__s)
        return super().write(__s)


class LogView(CustomWidget):
    """Лог"""

    def __init__(self) -> None:
        self._text = Text()
        super().__init__(ChildWindow().add(self._text))

        self._messages = list[str]()
        Logger.out = TextIOEchoAdapter(self._addMessage)

    def _addMessage(self, message: str) -> None:
        self._messages.append(message)
        self._text.setValue('\n'.join(self._messages))
