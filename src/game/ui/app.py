from tkinter import BOTH
from tkinter import HORIZONTAL
from tkinter import Tk
from tkinter import VERTICAL
from tkinter import ttk
from typing import ClassVar
from typing import Final

from game.core.environment import Environment
from game.ui.font import FontFactory
from game.ui.theme import Theme
from game.ui.widgets.resizablepanedwindow import ResizablePanedWindow
from game.ui.widgets.view.gameboard import GameBoardView
from game.ui.widgets.view.log import LogView
from game.ui.widgets.view.playerlist import PlayerListView


class App(Tk):
    """Главное окно приложения"""
    _update_interval_ms: ClassVar = 100

    def __init__(self, env: Environment) -> None:
        super().__init__()
        self.env: Final = env

        self.title("Game Monitor")
        self.geometry("1280x720")
        self._configure_styles()
        self._setup_ui()
        self._start_updates()

    def _configure_styles(self) -> None:
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

    def _setup_ui(self) -> None:
        """Инициализация пользовательского интерфейса"""
        # Главный контейнер с вертикальным разделением
        main_pane = ResizablePanedWindow(self, orient=VERTICAL)
        main_pane.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Верхняя панель (игровое поле + игроки)
        upper_pane = ResizablePanedWindow(main_pane, orient=HORIZONTAL)
        main_pane.add(upper_pane)

        # Игровое поле
        game_frame = ttk.LabelFrame(upper_pane, text="Игровое поле")
        self.board_view = GameBoardView(game_frame, self.env.board)
        self.board_view.pack(fill=BOTH, expand=True, padx=5, pady=5)
        upper_pane.add(game_frame)

        # Список игроков
        player_frame = ttk.LabelFrame(upper_pane, text="Игроки")
        self.player_view = PlayerListView(player_frame)
        self.player_view.pack(fill=BOTH, expand=True, padx=5, pady=5)
        upper_pane.add(player_frame)

        # Логи игры
        log_frame = ttk.LabelFrame(main_pane, text="Журнал")
        self.log_view = LogView(log_frame)
        self.log_view.pack(fill=BOTH, expand=True, padx=5, pady=5)
        main_pane.add(log_frame)

    def _start_updates(self) -> None:
        """Запустить цикл обновления интерфейса"""
        self.after(self._update_interval_ms, self._update_ui)

    def _update_ui(self) -> None:
        """Обновить все компоненты интерфейса"""
        self.player_view.update_players({
            str(mac): player for mac, player in self.env.players.items()
        })

        self.board_view.update_board()
        self.log_view.update_logs()
        self.after(self._update_interval_ms, self._update_ui)
