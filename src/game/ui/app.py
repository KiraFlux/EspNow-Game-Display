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
from game.ui.widgets.gameboardview import GameBoardView
from game.ui.widgets.logview import LogView
from game.ui.widgets.playerlistview import PlayerListView
from game.ui.widgets.resizablepanedwindow import ResizablePanedWindow


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
        style.configure(".", background=Theme.background, foreground=Theme.foreground)
        style.configure("TFrame", background=Theme.background)
        style.configure("TLabel", background=Theme.background, foreground=Theme.foreground)
        style.configure("TLabelframe", background=Theme.background, relief="flat")
        style.configure("TLabelframe.Label", background=Theme.background, foreground=Theme.accent)
        style.configure("TScrollbar", background=Theme.border)

        # Стиль для PanedWindow
        style.configure("TPanedWindow", background=Theme.border)

        # Кастомные стили
        style.configure("Secondary.TFrame", background=Theme.secondary_background)
        style.configure("Card.TFrame", background=Theme.card_background, relief="ridge")
        style.configure("Heading.TLabel", font=FontFactory.heading(), foreground=Theme.muted_text)
        style.configure("Normal.TLabel", font=FontFactory.body())
        style.configure("Muted.TLabel", font=FontFactory.small(), foreground=Theme.muted_text)
        style.configure("Accent.TLabel", font=FontFactory.body(), foreground=Theme.accent)

        # Настройка фона окна
        self.configure(bg=Theme.background)

    def _setup_ui(self) -> None:
        """Инициализация пользовательского интерфейса"""
        # Главный контейнер с вертикальным разделением
        main_pane = ResizablePanedWindow(self, orient=VERTICAL)
        main_pane.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Верхняя панель (игровое поле + игроки)
        upper_pane = ResizablePanedWindow(main_pane, orient=HORIZONTAL)
        main_pane.add(upper_pane)

        # Игровое поле
        game_frame = ttk.LabelFrame(upper_pane, text="ИГРОВОЕ ПОЛЕ")
        self.board_view = GameBoardView(game_frame, self.env.board)
        self.board_view.pack(fill=BOTH, expand=True, padx=5, pady=5)
        upper_pane.add(game_frame)

        # Список игроков
        player_frame = ttk.LabelFrame(upper_pane, text="ИГРОКИ")
        self.player_view = PlayerListView(player_frame)
        self.player_view.pack(fill=BOTH, expand=True, padx=5, pady=5)
        upper_pane.add(player_frame)

        # Логи игры
        log_frame = ttk.LabelFrame(main_pane, text="ЖУРНАЛ СОБЫТИЙ")
        self.log_view = LogView(log_frame)
        self.log_view.pack(fill=BOTH, expand=True, padx=5, pady=5)
        main_pane.add(log_frame)

        # Начальные позиции разделителей
        upper_pane.sashpos(0, self.winfo_width() * 2 // 3)
        main_pane.sashpos(0, self.winfo_height() * 3 // 4)

    def _start_updates(self) -> None:
        """Запустить цикл обновления интерфейса"""
        self.after(self._update_interval_ms, self._update_ui)

    def _update_ui(self) -> None:
        """Обновить все компоненты интерфейса"""
        self.player_view.update_players({
            str(mac): player for mac, player in self.env.players.items()
        })

        self.board_view.update_board(self.env.board)
        self.log_view.update_logs()
        self.after(self._update_interval_ms, self._update_ui)
