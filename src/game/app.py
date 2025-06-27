import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from typing import Final

from color import get_team_color
from color import get_text_color
from game.core.environment import Environment


class TkApp(tk.Tk):
    def __init__(self, game: Environment):
        super().__init__()
        self.game: Final = game
        self.title("Game Monitor")
        self.geometry("1280x720")
        self._setup_ui()
        self._start_updates()
        self._setup_menu()

    def _setup_menu(self):
        menu_bar = tk.Menu(self)

        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Выход", command=self.destroy)
        menu_bar.add_cascade(label="Файл", menu=file_menu)

        view_menu = tk.Menu(menu_bar, tearoff=0)
        view_menu.add_command(label="Обновить", command=self._update_ui)
        menu_bar.add_cascade(label="Вид", menu=view_menu)

        self.config(menu=menu_bar)

    def _setup_ui(self):
        main_pane = tk.PanedWindow(self, orient=tk.VERTICAL, sashrelief=tk.RAISED, sashwidth=4)
        main_pane.pack(fill=tk.BOTH, expand=True)

        upper_pane = tk.PanedWindow(main_pane, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=4)
        main_pane.add(upper_pane, stretch="always")

        game_frame = ttk.LabelFrame(upper_pane, text="Game Board")
        self.canvas = tk.Canvas(game_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        upper_pane.add(game_frame, stretch="always", width=600)

        player_frame = ttk.LabelFrame(upper_pane, text="Players")
        self.player_tree = ttk.Treeview(player_frame, columns=("MAC", "Username", "Team"), show="headings")
        self.player_tree.heading("MAC", text="MAC Address")
        self.player_tree.heading("Username", text="Username")
        self.player_tree.heading("Team", text="Team")
        self.player_tree.column("MAC", width=120)
        self.player_tree.column("Username", width=100)
        self.player_tree.column("Team", width=50)

        scrollbar = ttk.Scrollbar(player_frame, orient="vertical", command=self.player_tree.yview)
        self.player_tree.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")
        self.player_tree.pack(side="left", fill="both", expand=True)
        upper_pane.add(player_frame, width=300)

        log_frame = ttk.LabelFrame(main_pane, text="Game Logs")
        self.log_area = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD)
        self.log_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.log_area.config(state="disabled")
        main_pane.add(log_frame, height=150)

        upper_pane.sash_place(0, 600, 0)
        main_pane.sash_place(0, 0, 550)

    def _start_updates(self):
        self.after(100, self._update_ui)

    def _update_ui(self):
        self._update_players()
        self._update_board()
        self._update_logs()

        self.after(100, self._update_ui)

    def _update_players(self):
        expanded_items = []
        for item in self.player_tree.get_children():
            if self.player_tree.item(item, "open"):
                expanded_items.append(item)

        for item in self.player_tree.get_children():
            self.player_tree.delete(item)

        for mac, player in self.game.players.items():
            mac_str = mac.hex(':')
            item = self.player_tree.insert("", "end", values=(mac_str, player.username, player.team))

            if mac_str in expanded_items:
                self.player_tree.item(item, open=True)

    def _update_board(self):
        self.canvas.delete("all")

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        cell_size = min(width // 16, height // 16)

        offset_x = (width - cell_size * 16) // 2
        offset_y = (height - cell_size * 16) // 2

        for x in range(16):
            for y in range(16):
                x1 = offset_x + x * cell_size
                y1 = offset_y + y * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                team = self.game.board_state.get((x, y), 0)
                color = get_team_color(team)

                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline="#555555",
                    width=1
                )

                if team > 0:
                    self.canvas.create_text(
                        (x1 + x2) // 2,
                        (y1 + y2) // 2,
                        text=str(team),
                        fill=get_text_color(color),
                        font=("Arial", 10, "bold")
                    )

    def _update_logs(self):
        self.log_area.config(state="normal")

        while len(self.game.logs) > 0:
            log_msg = self.game.logs.pop(0)
            self.log_area.insert(tk.END, log_msg + "\n")

        self.log_area.config(state="disabled")
        self.log_area.yview(tk.END)

        if self.log_area.index(tk.END).split('.')[0] > '1000':
            self.log_area.delete('1.0', '500.0')
