from functools import cache

from game.impl.valuegen.color import ColorGenerator
from game.impl.valuegen.loopstep import LoopStepGenerator
from game.impl.valuegen.phasedamplitude import PhasedAmplitudeGenerator
from rs.color import Color

_team_color_gen = ColorGenerator(
    hue=LoopStepGenerator(
        start=15,
        step=200,
        loop=360,
    ),
    saturation=PhasedAmplitudeGenerator(
        scale=1.618,
        base=0.6,
        amplitude=0.2
    ),
    light=PhasedAmplitudeGenerator(
        scale=0.618,
        base=0.7,
        amplitude=0.2
    )
)


@cache
def get_team_color(team: int) -> Color:
    """Генерация уникального цвета для команды"""
    return _team_color_gen.calc(team)
