import tkinter as tk
from tkinter import ttk, scrolledtext
from dataclasses import dataclass
from threading import Thread
from typing import Optional
import queue
import time

from serialcmd.serializers import u16
from serialcmd.serializers import u8
from serialcmd.streams.abc import Stream
from serialcmd.streams.serials import Serial

# Глобальная очередь для логов
log_queue = queue.Queue()


def log(s: str):
    log_queue.put(s)


@dataclass
class Player:
    username: str
    team: int


class GameListener:
    def __init__(self) -> None:
        self.mac: Optional[bytes] = None
        self.players = dict[bytes, Player]()
        self.board = dict[tuple[int, int], int]()

        SendMac = 0x01
        LogOutput = 0x02
        BoardStateUpdate = 0x03
        PlayerListUpdate = 0x04

        self.jt = {
            SendMac: self.readMac,
            LogOutput: self.readLog,
            BoardStateUpdate: self.readBoardStateUpdate,
            PlayerListUpdate: self.readPlayerListUpdate,
        }

    def readMac(self, stream: Stream):
        self.mac = stream.read(6)
        return

    def readLog(self, stream: Stream):
        msg = stream.read(128)
        msg = msg.rstrip(b'\x00')
        try:
            log(f"LOG: {msg.decode()}")
        except UnicodeDecodeError as e:
            log(f"{e}: {msg.hex(sep='-', bytes_per_sep=2)}")
        return

    def readBoardStateUpdate(self, stream: Stream):
        length = u16.read(stream)
        for _ in range(length):
            x = u8.read(stream)
            y = u8.read(stream)
            team = u8.read(stream)
            self.board[(x, y)] = team
        return

    def readPlayerListUpdate(self, stream: Stream):
        length = u16.read(stream)
        for _ in range(length):
            mac = stream.read(6)
            username = stream.read(16).rstrip(b'\x00').decode()
            team = u8.read(stream)
            self.players[mac] = Player(username, team)
        return

    def run(self, stream: Stream) -> None:
        try:
            while True:
                opp = u8.read(stream)
                handler = self.jt.get(opp)
                if handler is not None:
                    handler(stream)
        except KeyboardInterrupt:
            return


class TkApp(tk.Tk):
    def __init__(self, listener: GameListener, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.listener = listener
        self.title("Game Monitor")
        self.geometry("1280x900")
        self._setup_ui()
        self._start_updates()

    def _setup_ui(self):
        # Main grid configuration
        self.grid_columnconfigure(0, weight=3, uniform="group1")
        self.grid_columnconfigure(1, weight=1, uniform="group1")
        self.grid_rowconfigure(0, weight=3)
        self.grid_rowconfigure(1, weight=1)

        # Game board canvas
        self.canvas = tk.Canvas(self, bg="white")
        self.canvas.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        # Player list frame
        player_frame = ttk.LabelFrame(self, text="Players")
        player_frame.grid(row=0, column=1, padx=5, pady=5, sticky="nsew")
        player_frame.grid_propagate(False)

        # Player treeview
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

        # Log frame
        log_frame = ttk.LabelFrame(self, text="Game Logs")
        log_frame.grid(row=1, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")

        # Log text area
        self.log_area = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD)
        self.log_area.pack(fill="both", expand=True)
        self.log_area.config(state="disabled")

    def _start_updates(self):
        self.after(100, self._update_ui)

    def _update_ui(self):
        # Update player list
        self._update_players()

        # Update game board
        self._update_board()

        # Update logs
        self._update_logs()

        self.after(100, self._update_ui)

    def _update_players(self):
        # Clear current data
        for item in self.player_tree.get_children():
            self.player_tree.delete(item)

        # Add new players
        for mac, player in self.listener.players.items():
            mac_str = mac.hex(':')
            self.player_tree.insert("", "end", values=(mac_str, player.username, player.team))

    def _update_board(self):
        self.canvas.delete("all")
        cell_size = 50

        # Draw grid
        for x in range(8):
            for y in range(8):
                x1 = x * cell_size
                y1 = y * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                # Get team color or default to gray
                team = self.listener.board.get((x, y), 0)
                color = self._get_team_color(team)

                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline="black"
                )

                # Draw coordinates (optional)
                self.canvas.create_text(
                    x1 + 10, y1 + 10,
                    text=f"{x},{y}",
                    fill="black" if team == 0 else "white"
                )

    def _get_team_color(self, team: int) -> str:
        colors = {
            0: "gray",  # Neutral/default
            1: "red",  # Team 1
            2: "blue",  # Team 2
            3: "green",  # Team 3
            4: "yellow",  # Team 4
        }
        return colors.get(team, "gray")

    def _update_logs(self):
        self.log_area.config(state="normal")
        while not log_queue.empty():
            try:
                log_msg = log_queue.get_nowait()
                self.log_area.insert(tk.END, log_msg + "\n")
            except queue.Empty:
                break
        self.log_area.config(state="disabled")
        self.log_area.yview(tk.END)


class App:
    def __init__(self):
        # Create game listener
        self.listener = GameListener()

        # Setup serial connection
        self.serial = Serial("COM8", 115200)

        # Start listener thread
        self.thread = Thread(target=self.listener.run, args=(self.serial,))
        self.thread.daemon = True
        self.thread.start()

        # Create and run Tkinter app
        self.tk_app = TkApp(self.listener)
        self.tk_app.mainloop()


if __name__ == "__main__":
    app = App()