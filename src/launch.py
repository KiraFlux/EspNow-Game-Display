from threading import Thread
from time import sleep
from typing import Callable

from bytelang.impl.stream.serials import SerialStream
from game.core.entities.mac import Mac
from game.core.entities.rules import GameRules
from game.core.entities.rules import ScoreRules
from game.core.environment import Environment
from game.core.protocol import GameProtocol
from game.impl.valuegen.color import ColorGenerator
from game.impl.valuegen.loopstep import LoopStepGenerator
from game.impl.valuegen.phasedamplitude import PhasedAmplitudeGenerator
from game.ui.app import GameApp
from rs.lina.vector import Vector2D
from rs.misc.log import Logger


def _create_task[T](f: Callable[[T], None], arg: T) -> Thread:
    return Thread(target=f, args=(arg,), daemon=True)


def _protocol_task(env: Environment):
    log = Logger("protocol-task")

    ports = SerialStream.getPorts()

    if not ports:
        log.write("Нет доступных портов, завершение")
        return

    log.write(f"Найдены порты: {ports}")

    stream = SerialStream(ports[0], 115200)
    protocol = GameProtocol(stream, env)

    protocol.request_mac(None)

    while True:
        result = protocol.pull()

        if result.is_err():
            log.write(result.err().unwrap())


def _agents_task(env: Environment):
    sleep(0.1)

    x = env.board.size.x // 2
    y = env.board.size.y

    for i in range(y):

        team = env.team_registry.register()

        for j in range(x):
            mac = Mac(bytes((0, 0, 0, 0, j % 255, i % 255)))

            env.onPlayerMessage(mac, f"User-{i}-{j}")

            player = env.player_registry.getAll().get(mac)
            player.setTeam(team)

            k = i * x + j

            env.onPlayerMove(mac, Vector2D(k % x, k // x))

    return


def _main():
    rules = GameRules(
        score=ScoreRules(
            mode=ScoreRules.CellLookupMode.Orthogonal,
            empty_cell=10,
            friend_cell=50,
            enemy_cell=-25
        ),
        team_color_generator=ColorGenerator(
            hue=LoopStepGenerator(
                start=15,
                step=200,
                loop=360,
            ),
            saturation=PhasedAmplitudeGenerator(
                scale=1.618,
                base=0.7,
                amplitude=0.2
            ),
            light=PhasedAmplitudeGenerator(
                scale=0.618,
                base=0.6,
                amplitude=0.2
            )
        ),
        move_cooldown_secs=5.0,
        move_available=True,
    )

    env = Environment(rules)

    GameApp(env).run("Game", 1280, 720, user_tasks=(
        # _create_task(_agents_task, env),
        _create_task(_protocol_task, env),
    ))


if __name__ == "__main__":
    _main()
