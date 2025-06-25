from threading import Thread

from game.app import TkApp
from game.core.player import GameInfo
from game.core.protocol import GameProtocolV1
from serialcmd.impl.stream.serials import SerialStream


def _listener_task(listener: GameProtocolV1):
    print('Senders')
    print('\n'.join(map(str, listener.getSenders())))
    print('Receivers')
    print('\n'.join(map(str, listener.getReceivers())))

    while True:
        result = listener.pull()

        if result.is_err():
            print(f"task pull: {result.err().unwrap()}")


def _main():

    game = GameInfo()

    serial = SerialStream("COM8", 115200)

    listener = GameProtocolV1(serial, game)

    task = Thread(target=_listener_task, args=(listener,), daemon=True)
    task.start()

    tk_app = TkApp(game)
    tk_app.mainloop()

    task.join()


if __name__ == "__main__":
    _main()
