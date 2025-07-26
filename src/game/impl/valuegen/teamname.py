from pathlib import Path
from typing import ClassVar
from typing import Final
from typing import Sequence

from game.abc.valuegen import ValueGenerator


class TeamNameGenerator(ValueGenerator[str]):
    """Генератор имён команд"""

    _core_filename: ClassVar = 'cores.txt'
    _prefix_filename: ClassVar = 'prefixes.txt'

    def __init__(self, team_name_folder: Path) -> None:
        self.cores: Final = self._read_words(team_name_folder / self._core_filename)
        self.prefixes: Final = self._read_words(team_name_folder / self._prefix_filename)

        self._total_cores: Final = len(self.cores)
        assert self._total_cores > 0

        _total_prefixes = len(self.prefixes)

        if self._total_cores == _total_prefixes:
            _total_prefixes -= 1

        self._total_prefixes: Final = _total_prefixes
        assert self._total_prefixes > 0

    @staticmethod
    def _read_words(filename: Path) -> Sequence[str]:
        with open(filename) as f:
            return tuple(filter(bool, (
                line.strip()
                for line in f
            )))

    def calc(self, x: int) -> str:
        index = x % (self._total_cores * self._total_prefixes)

        prefix_index = index % self._total_prefixes
        core_index = index % self._total_cores

        return f"{self.prefixes[prefix_index]} {self.cores[core_index]}"
