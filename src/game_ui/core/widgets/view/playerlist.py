from __future__ import annotations

from tkinter import BOTH
from tkinter import Canvas
from tkinter import Event
from tkinter import LEFT
from tkinter import Misc
from tkinter import RIGHT
from tkinter import X
from tkinter import Y
from tkinter import ttk

from game.core.entities import Player
from game_ui.core.widgets.playercard import PlayerCard
from tk_ui.core.theme import Theme


class PlayerListView(ttk.Frame):
    """Список игроков с возможностью прокрутки"""

    def __init__(self, master: Misc) -> None:
        super().__init__(master, style="Secondary.TFrame")
        self._setup_widgets()
        self.player_cards = dict[str, PlayerCard]()

    def _setup_widgets(self) -> None:
        """Настроить элементы интерфейса"""
        # Заголовок
        header = ttk.Label(
            self,
            text="ИГРОКИ",
            style="Heading.TLabel",
            anchor="w"
        )
        header.pack(fill=X, pady=(0, 8))

        # Контейнер для карточек
        container = ttk.Frame(self, style="Secondary.TFrame")
        container.pack(fill=BOTH, expand=True)

        # Полоса прокрутки
        self.scrollbar = ttk.Scrollbar(container, orient="vertical")
        self.scrollbar.pack(side=RIGHT, fill=Y)

        # Холст для прокрутки
        self.canvas = Canvas(
            container,
            yscrollcommand=self.scrollbar.set,
            bg=Theme.current().secondary_background.toHex(),
            highlightthickness=0
        )
        self.canvas.pack(side=LEFT, fill=BOTH, expand=True)
        self.scrollbar.config(command=self.canvas.yview)

        # Фрейм для карточек
        self.scrollable_frame = ttk.Frame(
            self.canvas,
            style="Secondary.TFrame"
        )
        self.scrollable_frame_id = self.canvas.create_window(
            (0, 0),
            window=self.scrollable_frame,
            anchor="nw"
        )

        # Привязка событий
        self.scrollable_frame.bind(
            "<Configure>",
            self._on_frame_configure
        )
        self.canvas.bind("<Configure>", self._on_canvas_configure)

    def _on_frame_configure(self, e: Event) -> None:
        """Обновить область прокрутки при изменении фрейма"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event: Event) -> None:
        """Обновить ширину фрейма при изменении холста"""
        self.canvas.itemconfig(self.scrollable_frame_id, width=event.width)

    def update_players(self, players: dict[str, Player]) -> None:
        """Обновить список игроков"""
        current_macs = set(self.player_cards.keys())
        new_macs = set(players.keys())

        # Удалить отсутствующих игроков
        for mac in current_macs - new_macs:
            self.player_cards[mac].destroy()
            del self.player_cards[mac]

        # Добавить/обновить игроков
        for mac, player in players.items():
            if mac not in self.player_cards:
                card = PlayerCard(self.scrollable_frame)
                card.pack(fill=X, pady=4, padx=2)
                self.player_cards[mac] = card

            self.player_cards[mac].update_player(mac, player)
