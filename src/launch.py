from queue import Queue
from threading import Thread

from game.core.app import TkApp
from game.core.listener import GameListener
from serialcmd.streams.serials import Serial


def _main():
    logs = Queue()

    listener = GameListener(logs.put)

    serial = Serial("COM19", 115200)

    task = Thread(target=listener.run, args=(serial,), daemon=True)
    task.start()

    tk_app = TkApp(listener, logs)
    tk_app.mainloop()

    task.join()


if __name__ == "__main__":
    _main()
