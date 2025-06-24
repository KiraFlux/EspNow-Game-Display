import queue
import tkinter as tk
from dataclasses import dataclass
from threading import Thread
from tkinter import scrolledtext
from tkinter import ttk
from typing import Optional

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
        print(self.mac.hex('-', 2))
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
        self.board.clear()

        length = u16.read(stream)

        for _ in range(length):
            x = u8.read(stream)
            y = u8.read(stream)
            team = u8.read(stream)
            self.board[(x, y)] = team
        return

    def readPlayerListUpdate(self, stream: Stream):
        self.players.clear()

        length = u16.read(stream)

        for _ in range(length):
            mac = stream.read(6)
            username = stream.read(32).rstrip(b'\x00').decode()
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
        self.geometry("1000x700")
        self._setup_ui()
        self._start_updates()
        self._setup_menu()

    def _setup_menu(self):
        menu_bar = tk.Menu(self)

        # Меню "Файл"
        file_menu = tk.Menu(menu_bar, tearoff=0)
        file_menu.add_command(label="Выход", command=self.destroy)
        menu_bar.add_cascade(label="Файл", menu=file_menu)

        # Меню "Вид"
        view_menu = tk.Menu(menu_bar, tearoff=0)
        view_menu.add_command(label="Обновить", command=self._update_ui)
        menu_bar.add_cascade(label="Вид", menu=view_menu)

        self.config(menu=menu_bar)

    def _setup_ui(self):
        # Создаем панель с разделителем для основной области и логов
        main_pane = tk.PanedWindow(self, orient=tk.VERTICAL, sashrelief=tk.RAISED, sashwidth=4)
        main_pane.pack(fill=tk.BOTH, expand=True)

        # Верхняя панель (игровое поле + список игроков)
        upper_pane = tk.PanedWindow(main_pane, orient=tk.HORIZONTAL, sashrelief=tk.RAISED, sashwidth=4)
        main_pane.add(upper_pane, stretch="always")

        # Игровое поле
        game_frame = ttk.LabelFrame(upper_pane, text="Game Board")
        self.canvas = tk.Canvas(game_frame, bg="white")
        self.canvas.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        upper_pane.add(game_frame, stretch="always", width=600)

        # Список игроков
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

        # Область логов
        log_frame = ttk.LabelFrame(main_pane, text="Game Logs")
        self.log_area = scrolledtext.ScrolledText(log_frame, wrap=tk.WORD)
        self.log_area.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        self.log_area.config(state="disabled")
        main_pane.add(log_frame, height=150)  # Начальная высота

        # Настройка пропорций разделителей
        upper_pane.sash_place(0, 600, 0)  # Позиция разделителя между игровым полем и списком игроков
        main_pane.sash_place(0, 0, 550)  # Позиция разделителя между основной областью и логами

    def _start_updates(self):
        self.after(100, self._update_ui)

    def _update_ui(self):
        # Обновление списка игроков
        self._update_players()

        # Обновление игрового поля
        self._update_board()

        # Обновление логов
        self._update_logs()

        self.after(100, self._update_ui)

    def _update_players(self):
        # Сохраняем текущее состояние развертывания
        expanded_items = []
        for item in self.player_tree.get_children():
            if self.player_tree.item(item, "open"):
                expanded_items.append(item)

        # Очищаем текущие данные
        for item in self.player_tree.get_children():
            self.player_tree.delete(item)

        # Добавляем новых игроков
        for mac, player in self.listener.players.items():
            mac_str = mac.hex(':')
            item = self.player_tree.insert("", "end", values=(mac_str, player.username, player.team))

            # Восстанавливаем состояние развертывания
            if mac_str in expanded_items:
                self.player_tree.item(item, open=True)

    def _update_board(self):
        self.canvas.delete("all")

        # Получаем текущие размеры холста
        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()

        # Рассчитываем размер клетки
        cell_size = min(width // 16, height // 16)

        # Центрируем поле на холсте
        offset_x = (width - cell_size * 16) // 2
        offset_y = (height - cell_size * 16) // 2

        # Рисуем сетку 16x16
        for x in range(16):
            for y in range(16):
                x1 = offset_x + x * cell_size
                y1 = offset_y + y * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                # Получаем цвет команды
                team = self.listener.board.get((x, y), 0)
                color = self._get_team_color(team)

                # Рисуем клетку
                self.canvas.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline="#555555",
                    width=1
                )

                # Добавляем номер команды (если не нейтральная)
                if team > 0:
                    self.canvas.create_text(
                        (x1 + x2) // 2,
                        (y1 + y2) // 2,
                        text=str(team),
                        fill=self._get_text_color(color),
                        font=("Arial", 10, "bold")
                    )

    def _get_team_color(self, team: int) -> str:
        # Расширенная палитра из 20 цветов
        colors = {
            0: "#CCCCCC",  # Нейтральный - светло-серый
            1: "#FF6B6B",  # Красный коралловый
            2: "#4ECDC4",  # Бирюзовый
            3: "#45B7D1",  # Голубой океан
            4: "#FFBE0B",  # Ярко-желтый
            5: "#FB5607",  # Оранжевый огненный
            6: "#8338EC",  # Фиолетовый электрик
            7: "#3A86FF",  # Ярко-синий
            8: "#06D6A0",  # Изумрудный
            9: "#118AB2",  # Темно-бирюзовый
            10: "#073B4C",  # Глубокий синий
            11: "#EF476F",  # Розовый фламинго
            12: "#FFD166",  # Золотистый
            13: "#8AC926",  # Свежая зелень
            14: "#7209B7",  # Фиолетовый драгоценный
            15: "#F15BB5",  # Горячий розовый
            16: "#9B5DE5",  # Лавандовый
            17: "#00BBF9",  # Яркий аквамарин
            18: "#00F5D4",  # Бирюзовый неоновый
            19: "#FEE440",  # Лимонный
            20: "#9B2226",  # Бордовый
        }
        return colors.get(team, "#CCCCCC")

    def _adjust_color(self, color: str, amount: int) -> str:
        """Осветление или затемнение цвета"""
        # Конвертация HEX в RGB
        r = int(color[1:3], 16)
        g = int(color[3:5], 16)
        b = int(color[5:7], 16)

        # Корректировка компонентов
        r = min(255, max(0, r + amount))
        g = min(255, max(0, g + amount))
        b = min(255, max(0, b + amount))

        # Конвертация обратно в HEX
        return f"#{r:02x}{g:02x}{b:02x}"

    def _get_text_color(self, bg_color: str) -> str:
        """Определение цвета текста на основе фона"""
        # Конвертация HEX в RGB
        r = int(bg_color[1:3], 16)
        g = int(bg_color[3:5], 16)
        b = int(bg_color[5:7], 16)

        # Рассчет яркости (формула W3C)
        brightness = (r * 299 + g * 587 + b * 114) / 1000
        return "#000000" if brightness > 128 else "#FFFFFF"

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

        # Автоматическое обрезание старых логов
        if self.log_area.index(tk.END).split('.')[0] > '1000':
            self.log_area.delete('1.0', '500.0')


class App:
    def __init__(self):
        # Создаем слушатель игры
        self.listener = GameListener()

        # Настраиваем последовательное соединение
        self.serial = Serial("COM19", 115200)

        # Запускаем поток слушателя
        self.thread = Thread(target=self.listener.run, args=(self.serial,))
        self.thread.daemon = True
        self.thread.start()

        # Создаем и запускаем Tkinter приложение
        self.tk_app = TkApp(self.listener)
        self.tk_app.mainloop()


if __name__ == "__main__":
    app = App()
