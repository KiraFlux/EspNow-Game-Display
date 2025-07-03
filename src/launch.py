from threading import Thread
from typing import Callable

from bytelang.impl.stream.serials import SerialStream
from game.core.entities.mac import Mac
from game.core.environment import Environment
from game.core.protocol import GameProtocol
from game.ui.app import GameApp
from lina.vector import Vector2D
from misc.log import Logger


def _start_task[T](f: Callable[[T], None], arg: T) -> Thread:
    return Thread(target=f, args=(arg,), daemon=True)


def _protocol_task(protocol: GameProtocol):
    log = Logger.inst().sub("task")

    protocol.request_mac(None)

    while True:
        result = protocol.pull()

        if result.is_err():
            log.write(result.err().unwrap())


def _create_protocol_task(env: Environment) -> Thread:
    stream = SerialStream("COM8", 115200)
    protocol = GameProtocol(stream, env)

    return _start_task(_protocol_task, protocol)


def _agents_task(env: Environment):
    for i in range(30):
        mac = Mac(bytes((0, 0, 0, 0, 0, i)))
        env.onPlayerMessage(mac, f"User-{i}")

        env.onPlayerMove(mac, Vector2D(i % env.board.size.x, i // env.board.size.x))

    # for i in range(10):
    #     env.onPlayerMessage(Mac(bytes((0, 0, 0, 0, 0, 0))), f"Cool_Name_{i}")
    #     sleep(1)

    return


def _create_agents_task(env: Environment):
    return _start_task(_agents_task, env)


def _main():
    environment = Environment()

    # _launch_protocol(environment)

    GameApp(environment).run("Game", 1280, 720, user_tasks=(
        _create_agents_task(environment),
    ))


if __name__ == "__main__":
    _main()
