from abc import ABC
from abc import abstractmethod
from tkinter import Tk
from tkinter import ttk
from typing import ClassVar

from tk_ui.core.font import FontFactory
from tk_ui.core.theme import Theme


class App(Tk, ABC):
    """Tk wrapper"""

    _update_interval_ms: ClassVar = 200

    def __init__(self) -> None:
        super().__init__()
        self.__configure_styles()

    @abstractmethod
    def onUpdate(self) -> None:
        """При обновлении UI"""

    def startUpdates(self) -> None:
        """Запустить обновления UI"""
        self.after(self._update_interval_ms, self.__update_ui)

    def setSize(self, width: int, height: int) -> None:
        """Установить размер окна"""
        self.geometry(f"{width}x{height}")

    def __configure_styles(self) -> None:
        """Настроить стили для тёмной темы"""
        style = ttk.Style()

        # Базовая конфигурация
        style.configure(".", background=Theme.current().background.toHex(), foreground=Theme.current().foreground.toHex())
        style.configure("TFrame", background=Theme.current().background.toHex())
        style.configure("TLabel", background=Theme.current().background.toHex(), foreground=Theme.current().foreground.toHex())
        style.configure("TLabelframe", background=Theme.current().background.toHex(), relief="flat")
        style.configure("TLabelframe.Label", background=Theme.current().background.toHex(), foreground=Theme.current().accent.toHex())
        style.configure("TScrollbar", background=Theme.current().border.toHex())

        # Стиль для PanedWindow
        style.configure("TPanedWindow", background=Theme.current().border.toHex())

        # Кастомные стили
        style.configure("Secondary.TFrame", background=Theme.current().secondary_background)
        style.configure("Card.TFrame", background=Theme.current().card_background.toHex(), relief="ridge")
        style.configure("Heading.TLabel", font=FontFactory.heading(), foreground=Theme.current().muted_text.toHex())
        style.configure("Normal.TLabel", font=FontFactory.body())
        style.configure("Muted.TLabel", font=FontFactory.small(), foreground=Theme.current().muted_text)
        style.configure("Accent.TLabel", font=FontFactory.body(), foreground=Theme.current().accent.toHex())

        # Настройка фона окна
        self.configure(bg=Theme.current().background.toHex())

    def __update_ui(self) -> None:
        self.onUpdate()
        self.after(self._update_interval_ms, self.__update_ui)
