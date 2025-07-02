from tkinter import BOTH
from tkinter import HORIZONTAL
from tkinter import VERTICAL
from tkinter import ttk
from typing import Final

from game.core.environment import Environment
from tk_ui.core.widgets.resizablepanedwindow import ResizablePanedWindow
from tk_game_ui.core.widgets.view.gameboard import GameBoardView
from tk_game_ui.core.widgets.view.log import LogView
from tk_game_ui.core.widgets.view.playerlist import PlayerListView
from tk_ui.abc.app import App


class TkGameApp(App):
    """Главное окно приложения"""

    def __init__(self, env: Environment) -> None:
        super().__init__()
        self._env: Final = env

        # todo упростить

        # Главный контейнер с вертикальным разделением
        main_pane = ResizablePanedWindow(self, orient=VERTICAL)
        main_pane.pack(fill=BOTH, expand=True, padx=10, pady=10)

        # Верхняя панель (игровое поле + игроки)
        upper_pane = ResizablePanedWindow(main_pane, orient=HORIZONTAL)
        main_pane.add(upper_pane)

        # Игровое поле
        game_frame = ttk.LabelFrame(upper_pane, text="Игровое поле")
        self.board_view = GameBoardView(game_frame, self._env.board)
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

        self.startUpdates()

    def onUpdate(self) -> None:
        self.player_view.update_players({
            str(mac): player for mac, player in self._env.players.items()
        })

        self.board_view.update_board()
        self.log_view.update_logs()
