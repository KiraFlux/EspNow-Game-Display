from dataclasses import dataclass

from rs.color import Color


@dataclass
class Team:
    """Команда"""

    _color: Color
