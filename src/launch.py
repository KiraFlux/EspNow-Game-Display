from queue import Queue
from threading import Thread

from game.app import TkApp
from game.core.protocol import GameProtocol
from serialcmd.impl.stream.serials import SerialStream


def _listener_task(listener: GameProtocol):
    serial = SerialStream("COM19", 115200)

    while True:
        listener.pull(serial)


def _main():
    logs = Queue()

    listener = GameProtocol(logs.put)

    task = Thread(target=listener.pull, args=(listener,), daemon=True)
    # task.start()

    tk_app = TkApp(listener, logs)
    tk_app.mainloop()

    # task.join()


if __name__ == "__main__":
    _main()
