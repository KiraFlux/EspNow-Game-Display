from __future__ import annotations

from tkinter import LEFT
from tkinter import Misc
from tkinter import RIGHT
from tkinter import X
from tkinter import ttk

from game.core.entities import Mac
from game.core.entities import Player


class PlayerCard(ttk.Frame):
    """Карточка для отображения информации об игроке"""

    def __init__(self, master: Misc) -> None:
        super().__init__(master, style="Card.TFrame")
        self._setup_widgets()

    def _setup_widgets(self) -> None:
        """Создать элементы интерфейса"""
        # MAC-адрес
        self.mac_label = ttk.Label(
            self,
            style="Muted.TLabel",
            anchor="w"
        )
        self.mac_label.pack(fill=X)

        # Основная информация
        info_frame = ttk.Frame(self)
        info_frame.pack(fill=X, pady=(2, 0))

        self.username_label = ttk.Label(
            info_frame,
            style="Normal.TLabel",
            anchor="w"
        )
        self.username_label.pack(side=LEFT, fill=X, expand=True)

        self.team_label = ttk.Label(
            info_frame,
            style="Accent.TLabel",
            anchor="e",
        )
        self.team_label.pack(side=RIGHT, padx=(5, 0))

    def update_player(self, mac: Mac, player: Player) -> None:
        """Обновить данные игрока"""
        self.mac_label.config(text=f"MAC: {mac}")
        self.username_label.config(text=f"{player.username} ({player.score})")
        self.team_label.config(text=f"Команда: {player.team}")
