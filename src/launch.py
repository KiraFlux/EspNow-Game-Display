from threading import Thread

from game.core.player import GameInfo
from game.core.protocol import GameProtocol
from serialcmd.impl.stream.serials import SerialStream


def _listener_task(protocol: GameProtocol):
    protocol.request_mac(None)

    while True:
        result = protocol.pull()

        if result.is_err():
            print(f"task pull: {result.err().unwrap()}")

        if protocol.game.logs:
            print(protocol.game.logs.pop(0))

def _main():
    game = GameInfo()

    serial = SerialStream("COM8", 115200)

    listener = GameProtocol(serial, game)

    task = Thread(target=_listener_task, args=(listener,), daemon=True)
    task.start()

    # tk_app = TkApp(game)
    # tk_app.mainloop()

    task.join()


if __name__ == "__main__":
    _main()
