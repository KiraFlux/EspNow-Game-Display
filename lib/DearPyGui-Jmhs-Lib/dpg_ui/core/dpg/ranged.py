from abc import ABC

from dpg_ui.abc.ranged import Ranged
from dpg_ui.core.dpg.valued import DpgValuedWidget


class DpgRangedValuedWidget[T](DpgValuedWidget[T], Ranged[T], ABC):
    """Виджет DPG имеет диапазон и значение"""

    def _onRangeMaxChanged(self, new_max: T) -> None:
        self.configure(max_value=new_max)

    def _onRangeMinChanged(self, new_min: T) -> None:
        self.configure(min_value=new_min)
