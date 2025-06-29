from tkinter import Event
from tkinter import HORIZONTAL
from tkinter import Misc
from tkinter import ttk

from misc.vector import Vector2D


class ResizablePanedWindow(ttk.PanedWindow):
    """Панель с перетаскиваемыми разделителями"""

    def __init__(self, master: Misc, orient: str = HORIZONTAL, **kwargs) -> None:
        super().__init__(master, orient=orient, **kwargs)
        self.bind("<ButtonPress-1>", self.on_press)
        self.bind("<B1-Motion>", self.on_drag)
        self.bind("<ButtonRelease-1>", self.on_release)
        self._drag_start = Vector2D(0, 0)

    def on_press(self, e: Event) -> None:
        """Запомнить начальную позицию"""
        self._drag_start = Vector2D(e.x, e.y)

    def on_drag(self, e: Event) -> None:
        """Обработка перетаскивания разделителя"""
        dx = e.x - self._drag_start.x
        dy = e.y - self._drag_start.y

        if self.cget("orient") == HORIZONTAL:
            self.sashpos(0, self.sashpos(0) + dx)
        else:
            self.sashpos(0, self.sashpos(0) + dy)

        self._drag_start = Vector2D(e.x, e.y)

    def on_release(self, e: Event) -> None:
        """Обновить интерфейс после изменения"""
        self.master.update_idletasks()
