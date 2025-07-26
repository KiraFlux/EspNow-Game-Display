from pathlib import Path

from game.impl.valuegen.teamname import TeamNameGenerator

p = r"A:\Projects\EspNow-Game-Display\res\text\team-name"

t = TeamNameGenerator(Path(p))

for i in range(10000):
    print(f"{i:3} {t.calc(i)}")
