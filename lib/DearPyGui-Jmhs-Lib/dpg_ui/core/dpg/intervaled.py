from abc import ABC

from dpg_ui.abc.intervaled import Intervaled
from dpg_ui.core.dpg.valued import DpgValuedWidget


class DpgIntervaledValuedWidget[T](DpgValuedWidget[T], Intervaled[T], ABC):
    """Виджет DPG имеет диапазон и значение"""

    def _onIntervalMaxChanged(self, new_max: T) -> None:
        self.configure(max_value=new_max)

    def _onIntervalMinChanged(self, new_min: T) -> None:
        self.configure(min_value=new_min)
