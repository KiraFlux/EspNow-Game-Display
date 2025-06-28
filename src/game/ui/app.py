from __future__ import annotations

import tkinter as tk
from tkinter import scrolledtext
from tkinter import ttk
from typing import ClassVar, Dict, Final, Optional, Tuple

from color import get_team_color, get_text_color
from game.core.entities import Player, Vector2D
from game.core.environment import Board, Environment
from game.core.log import Logger

# Цветовая схема в стиле Discord
BG_COLOR: Final = "#36393f"
FG_COLOR: Final = "#ffffff"
SECONDARY_BG: Final = "#2f3136"
ACCENT_COLOR: Final = "#7289da"
BORDER_COLOR: Final = "#202225"
CARD_BG: Final = "#40444b"
MUTED_TEXT: Final = "#b9bbbe"


# Класс для управления шрифтами
class FontFactory:
    """Фабрика для создания согласованных шрифтов"""
    BASE_FONT: Final = "Segoe UI"
    MONO_FONT: Final = "Consolas"

    @classmethod
    def heading(cls, size: int = 14) -> Tuple[str, int, str]:
        """Шрифт для заголовков"""
        return (cls.BASE_FONT, size, "bold")

    @classmethod
    def body(cls, size: int = 11) -> Tuple[str, int, str]:
        """Основной шрифт для текста"""
        return (cls.BASE_FONT, size, "normal")

    @classmethod
    def mono(cls, size: int = 10) -> Tuple[str, int, str]:
        """Моноширинный шрифт для логов"""
        return (cls.MONO_FONT, size, "normal")

    @classmethod
    def small(cls) -> Tuple[str, int, str]:
        """Мелкий текст"""
        return (cls.BASE_FONT, 9, "normal")


# Класс для панелей с изменяемыми размерами
class ResizablePanedWindow(ttk.PanedWindow):
    """Панель с перетаскиваемыми разделителями"""

    def __init__(self, master: tk.Misc, orient: str = tk.HORIZONTAL, **kwargs) -> None:
        super().__init__(master, orient=orient, **kwargs)
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_release)
        self._drag_start = Vector2D(0, 0)

    def on_press(self, event: tk.Event) -> None:
        """Запомнить начальную позицию"""
        self._drag_start = Vector2D(event.x, event.y)

    def on_drag(self, event: tk.Event) -> None:
        """Обработка перетаскивания разделителя"""
        dx = event.x - self._drag_start.x
        dy = event.y - self._drag_start.y

        if self.cget("orient") == tk.HORIZONTAL:
            self.sashpos(0, self.sashpos(0) + dx)
        else:
            self.sashpos(0, self.sashpos(0) + dy)

        self._drag_start = Vector2D(event.x, event.y)

    def on_release(self, event: tk.Event) -> None:
        """Обновить интерфейс после изменения"""
        self.master.update_idletasks()


# Виджет для отображения логов
class LogView(scrolledtext.ScrolledText):
    """Виджет для отображения логов игры"""
    MAX_LINES: ClassVar = 1000
    TRUNCATE_LINES: ClassVar = 500

    def __init__(self, master: tk.Misc) -> None:
        super().__init__(
            master,
            wrap=tk.WORD,
            state="disabled",
            bg=SECONDARY_BG,
            fg=FG_COLOR,
            insertbackground=FG_COLOR,
            font=FontFactory.mono(),
            padx=10,
            pady=10
        )

    def update_logs(self) -> None:
        """Обновить содержимое логов"""
        self.config(state="normal")

        # Добавляем все доступные сообщения из глобального логгера
        while Logger.available():
            self.insert(tk.END, Logger.read() + "\n")

        self.config(state="disabled")
        self.yview(tk.END)

        # Автоочистка старых сообщений
        line_count = int(self.index(tk.END).split('.')[0])
        if line_count > self.MAX_LINES:
            self.delete('1.0', f"{self.TRUNCATE_LINES}.0")


# Карточка игрока
class PlayerCard(ttk.Frame):
    """Карточка для отображения информации об игроке"""

    def __init__(self, master: tk.Misc) -> None:
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
        self.mac_label.pack(fill=tk.X)

        # Основная информация
        info_frame = ttk.Frame(self)
        info_frame.pack(fill=tk.X, pady=(2, 0))

        self.username_label = ttk.Label(
            info_frame,
            style="Normal.TLabel",
            anchor="w"
        )
        self.username_label.pack(side=tk.LEFT, fill=tk.X, expand=True)

        self.team_label = ttk.Label(
            info_frame,
            style="Accent.TLabel",
            anchor="e"
        )
        self.team_label.pack(side=tk.RIGHT, padx=(5, 0))

    def update_player(self, mac: str, username: str, team: int) -> None:
        """Обновить данные игрока"""
        self.mac_label.config(text=f"MAC: {mac}")
        self.username_label.config(text=username)
        self.team_label.config(text=f"Команда: {team}")


# Список игроков с прокруткой
class PlayerListView(ttk.Frame):
    """Список игроков с возможностью прокрутки"""

    def __init__(self, master: tk.Misc) -> None:
        super().__init__(master, style="Secondary.TFrame")
        self._setup_widgets()
        self.player_cards: Dict[str, PlayerCard] = {}

    def _setup_widgets(self) -> None:
        """Настроить элементы интерфейса"""
        # Заголовок
        header = ttk.Label(
            self,
            text="ИГРОКИ",
            style="Heading.TLabel",
            anchor="w"
        )
        header.pack(fill=tk.X, pady=(0, 8))

        # Контейнер для карточек
        container = ttk.Frame(self, style="Secondary.TFrame")
        container.pack(fill=tk.BOTH, expand=True)

        # Полоса прокрутки
        self.scrollbar = ttk.Scrollbar(container, orient="vertical")
        self.scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Холст для прокрутки
        self.canvas = tk.Canvas(
            container,
            yscrollcommand=self.scrollbar.set,
            bg=SECONDARY_BG,
            highlightthickness=0
        )
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
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

    def _on_frame_configure(self, event: tk.Event) -> None:
        """Обновить область прокрутки при изменении фрейма"""
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def _on_canvas_configure(self, event: tk.Event) -> None:
        """Обновить ширину фрейма при изменении холста"""
        self.canvas.itemconfig(self.scrollable_frame_id, width=event.width)

    def update_players(self, players: Dict[str, Player]) -> None:
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
                card.pack(fill=tk.X, pady=4, padx=2)
                self.player_cards[mac] = card

            self.player_cards[mac].update_player(mac, player.username, player.team)


# Виджет игрового поля
class GameBoardView(tk.Canvas):
    """Виджет для отображения игрового поля"""

    def __init__(self, master: tk.Misc, board: Board) -> None:
        super().__init__(
            master,
            bg=SECONDARY_BG,
            highlightthickness=0
        )
        self._board = board
        self.bind("<Configure>", self._on_resize)

    def update_board(self, board: Board) -> None:
        """Обновить игровое поле"""
        self._board = board
        self._draw_board()

    def _on_resize(self, event: tk.Event) -> None:
        """Перерисовать поле при изменении размера"""
        self._draw_board()

    def _draw_board(self) -> None:
        """Отрисовать игровое поле"""
        self.delete("all")

        width = self.winfo_width()
        height = self.winfo_height()
        cx, cy = self._board.size.x, self._board.size.y

        if cx == 0 or cy == 0:
            return

        cell_size = min(width // cx, height // cy)
        offset_x = (width - cell_size * cx) // 2
        offset_y = (height - cell_size * cy) // 2

        # Отрисовка всех ячеек
        board_state = self._board.getState()
        for x in range(cx):
            for y in range(cy):
                pos = Vector2D(x, y)
                cell = board_state.get(pos)
                team = 0
                if cell is not None and cell.owner is not None:
                    team = cell.owner.team

                # Отрисовка ячейки
                x1 = offset_x + x * cell_size
                y1 = offset_y + y * cell_size
                x2 = x1 + cell_size
                y2 = y1 + cell_size

                color = get_team_color(team)
                self.create_rectangle(
                    x1, y1, x2, y2,
                    fill=color,
                    outline=BORDER_COLOR,
                    width=1
                )

                if team > 0:
                    self.create_text(
                        (x1 + x2) // 2, (y1 + y2) // 2,
                        text=str(team),
                        fill=get_text_color(color),
                        font=FontFactory.heading(10)
                    )


# Главное окно приложения
class App(tk.Tk):
    """Главное окно приложения"""
    UPDATE_INTERVAL_MS: ClassVar = 100

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
        style.configure(".", background=BG_COLOR, foreground=FG_COLOR)
        style.configure("TFrame", background=BG_COLOR)
        style.configure("TLabel", background=BG_COLOR, foreground=FG_COLOR)
        style.configure("TLabelframe", background=BG_COLOR, relief="flat")
        style.configure("TLabelframe.Label", background=BG_COLOR, foreground=ACCENT_COLOR)
        style.configure("TScrollbar", background=BORDER_COLOR)

        # Стиль для PanedWindow
        style.configure("TPanedWindow", background=BORDER_COLOR)

        # Кастомные стили
        style.configure("Secondary.TFrame", background=SECONDARY_BG)
        style.configure("Card.TFrame", background=CARD_BG, relief="ridge")
        style.configure("Heading.TLabel", font=FontFactory.heading(12), foreground=MUTED_TEXT)
        style.configure("Normal.TLabel", font=FontFactory.body())
        style.configure("Muted.TLabel", font=FontFactory.small(), foreground=MUTED_TEXT)
        style.configure("Accent.TLabel", font=FontFactory.body(10), foreground=ACCENT_COLOR)

        # Настройка фона окна
        self.configure(bg=BG_COLOR)

    def _setup_ui(self) -> None:
        """Инициализация пользовательского интерфейса"""
        # Главный контейнер с вертикальным разделением
        main_pane = ResizablePanedWindow(self, orient=tk.VERTICAL)
        main_pane.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Верхняя панель (игровое поле + игроки)
        upper_pane = ResizablePanedWindow(main_pane, orient=tk.HORIZONTAL)
        main_pane.add(upper_pane)

        # Игровое поле
        game_frame = ttk.LabelFrame(upper_pane, text="ИГРОВОЕ ПОЛЕ")
        self.board_view = GameBoardView(game_frame, self.env.board)
        self.board_view.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        upper_pane.add(game_frame)

        # Список игроков
        player_frame = ttk.LabelFrame(upper_pane, text="ИГРОКИ")
        self.player_view = PlayerListView(player_frame)
        self.player_view.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        upper_pane.add(player_frame)

        # Логи игры
        log_frame = ttk.LabelFrame(main_pane, text="ЖУРНАЛ СОБЫТИЙ")
        self.log_view = LogView(log_frame)
        self.log_view.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        main_pane.add(log_frame)

        # Начальные позиции разделителей
        upper_pane.sashpos(0, self.winfo_width() * 2 // 3)
        main_pane.sashpos(0, self.winfo_height() * 3 // 4)

    def _start_updates(self) -> None:
        """Запустить цикл обновления интерфейса"""
        self.after(self.UPDATE_INTERVAL_MS, self._update_ui)

    def _update_ui(self) -> None:
        """Обновить все компоненты интерфейса"""
        # Обновление списка игроков
        self.player_view.update_players({
            str(mac): player for mac, player in self.env.players.items()
        })

        # Обновление игрового поля
        self.board_view.update_board(self.env.board)

        # Обновление логов
        self.log_view.update_logs()

        # Планирование следующего обновления
        self.after(self.UPDATE_INTERVAL_MS, self._update_ui)