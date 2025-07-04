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
from lina.vector import Vector2D
from misc.log import Logger


def _create_task[T](f: Callable[[T], None], arg: T) -> Thread:
    return Thread(target=f, args=(arg,), daemon=True)


def _protocol_task(protocol: GameProtocol):
    log = Logger("protocol-task")

    protocol.request_mac(None)

    while True:
        result = protocol.pull()

        if result.is_err():
            log.write(result.err().unwrap())


def _create_protocol_task(env: Environment) -> Thread:
    stream = SerialStream("COM8", 115200)
    protocol = GameProtocol(stream, env)

    return _create_task(_protocol_task, protocol)


def _agents_task(env: Environment):
    for i in range(10):
        mac = Mac(bytes((0, 0, 0, 0, 0, i)))

        env.onPlayerMessage(mac, f"User-{i}")

        team = env.team_registry.register(f"Team-{i}")

        player = env.player_registry.getPlayers().get(mac)
        player.team = team

        env.onPlayerMove(mac, Vector2D(i % env.board.size.x, i // env.board.size.x))

        sleep(1)

    return


def _create_agents_task(env: Environment):
    return _create_task(_agents_task, env)


def _main():
    rules = GameRules(
        score=ScoreRules(
            friend_cell=25,
            enemy_cell=-50
        ),
        player_move_cooldown_secs=2.0,
        team_color_generator=ColorGenerator(
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
    )

    env = Environment(rules)

    GameApp(env).run("Game", 1280, 720, user_tasks=(
        _create_agents_task(env),
        # _create_protocol_task(env)
    ))


if __name__ == "__main__":
    _main()
