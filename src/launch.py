from threading import Thread

from game.core.environment import Environment
from game.core.log import Logger
from game.core.protocol import GameProtocol
from serialcmd.impl.stream.serials import SerialStream


def _listener_task(protocol: GameProtocol):
    root = Logger.inst()

    task = root.sub("task")

    protocol.request_mac(None)

    while True:
        result = protocol.pull()

        if result.is_err():
            task.write(result.err().unwrap())

        if root.available():
            print(root.read())


def _main():
    environment = Environment()

    serial = SerialStream("COM8", 115200)

    listener = GameProtocol(serial, environment)

    task = Thread(target=_listener_task, args=(listener,), daemon=True)
    task.start()

    # tk_app = TkApp(environment)
    # tk_app.mainloop()

    task.join()


if __name__ == "__main__":
    _main()
