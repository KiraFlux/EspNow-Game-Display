from __future__ import annotations

from kf_dpg.core.app import App
from kf_dpg.impl.containers import ChildWindow
from kf_dpg.impl.containers import Window
from kf_dpg.impl.sliders import IntSlider

w = Window("")

c = ChildWindow(_width=100, _height=300)

(
    w
    .add(c)
    .add(IntSlider("Width", interval=(100, 500), default=c.getWidth(), on_change=c.setWidth))
    .add(IntSlider("Height", interval=(100, 500), default=c.getHeight(), on_change=c.setHeight))
)

#
App(w).run("title", 1280, 720)
