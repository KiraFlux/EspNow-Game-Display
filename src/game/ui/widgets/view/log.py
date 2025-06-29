from tkinter import END
from tkinter import Misc
from tkinter import WORD
from tkinter import scrolledtext
from typing import ClassVar

from misc.log import Logger
from ui.core.font import FontFactory
from ui.core.theme import Theme


class LogView(scrolledtext.ScrolledText):
    """Виджет для отображения логов игры"""

    _max_lines: ClassVar = 1000
    _truncate_lines: ClassVar = 500

    def __init__(self, master: Misc) -> None:
        super().__init__(
            master,
            wrap=WORD,
            state="disabled",
            bg=Theme.current().secondary_background.toHex(),
            fg=Theme.current().foreground.toHex(),
            insertbackground=Theme.current().foreground.toHex(),
            font=FontFactory.mono(),
            padx=10,
            pady=10
        )

    def update_logs(self) -> None:
        """Обновить содержимое логов"""
        self.config(state="normal")

        while Logger.available():
            self.insert(END, Logger.read() + "\n")

        self.config(state="disabled")
        self.yview(END)

        line_count = int(self.index(END).split('.')[0])
        if line_count > self._max_lines:
            self.delete('1.0', f"{self._truncate_lines}.0")
