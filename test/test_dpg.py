from __future__ import annotations

from dataclasses import dataclass

import dearpygui.dearpygui as dpg

from dpg_ui.impl.button import Button
from dpg_ui.impl.display.text import DisplayText
from dpg_ui.impl.input.text import InputText
from dpg_ui.impl.slider.float_ import FloatSlider
from dpg_ui.impl.window import Window


@dataclass(frozen=True)
class App:
    """Приложение Dear Py Gui"""

    window: Window

    def run(self, title: str, width: int, height: int) -> None:
        """Запуск"""

        x = (1920 - width) // 2
        y = (1080 - height) // 2

        dpg.create_context()
        dpg.create_viewport(
            title=title,
            width=width,
            height=height,
            x_pos=x,
            y_pos=y,
        )

        # noinspection PyTypeChecker
        self.window.render(None)

        dpg.set_primary_window(self.window.tag(), True)

        dpg.setup_dearpygui()
        dpg.show_viewport()
        dpg.start_dearpygui()
        dpg.destroy_context()

    @staticmethod
    def setTitle(title: str) -> None:
        """Установить заголовок окна"""
        dpg.set_viewport_title(title)

    @staticmethod
    def setSize(width: int, height: int) -> None:
        """Установить размер окна"""
        dpg.set_viewport_width(width)
        dpg.set_viewport_height(height)

    @classmethod
    def getSize(cls) -> tuple[int, int]:
        """Получить размер окна"""
        return (
            cls.getWidth(),
            cls.getHeight()
        )

    @staticmethod
    def getWidth() -> int:
        """Получить ширину окна"""
        return dpg.get_viewport_width()

    @staticmethod
    def getHeight() -> int:
        """Получить высоту окна"""
        return dpg.get_viewport_height()

    @staticmethod
    def setPosition(x: float, y: float) -> None:
        """Установить позицию окна"""
        dpg.set_viewport_pos([x, y])

    @staticmethod
    def getPosition() -> tuple[float, float]:
        """Получить позицию окна"""
        x, y = dpg.get_viewport_pos()
        return x, y


__w = (
    Window("Text window")
    .add(DisplayText(_value_default="text"))
    .add(Button("Button"))
    .add(Button("Button"))
    .add(InputText("string", print))
    .add(FloatSlider("float", _value_default=0.123, _range_max=10, _range_min=-10))
)

App(__w).run("title", 1280, 720)
