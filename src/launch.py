from threading import Thread

from bytelang.impl.stream.serials import SerialStream
from game.core.environment import Environment
from game.core.protocol import GameProtocol
from tk_game_ui.impl.app.gameapp import GameApp
from misc.log import Logger


def _protocol_task(protocol: GameProtocol):
    log = Logger.inst().sub("task")

    protocol.request_mac(None)

    while True:
        result = protocol.pull()

        if result.is_err():
            log.write(result.err().unwrap())


def _launch_protocol(env: Environment):
    stream = SerialStream("COM8", 115200)
    protocol = GameProtocol(stream, env)

    task = Thread(target=_protocol_task, args=(protocol,), daemon=True)
    task.start()


def _main():
    environment = Environment()

    # _launch_protocol(environment)

    from game.core.entities import Mac

    for i in range(8):
        mac = Mac(bytes((0, 0, 0, 0, 0, i)))
        from lina.vector import Vector2D
        environment.onPlayerMessage(mac, f"User-{i}")
        environment.onPlayerMove(mac, Vector2D(i % environment.board.size.x, i // environment.board.size.x))

    app = GameApp(environment)
    app.setSize(1280, 720)
    app.title("Игра")
    app.mainloop()


if __name__ == "__main__":
    _main()
