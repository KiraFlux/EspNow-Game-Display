from threading import Thread

from game.core.player import GameInfo
from game.core.protocol import GameProtocol
from serialcmd.core.protocol import Protocol
from serialcmd.impl.stream.serials import SerialStream


def _listener_task(listener: Protocol):
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

    serial = SerialStream("COM19", 115200)

    listener = GameProtocol(serial, game)

    task = Thread(target=_listener_task, args=(listener,), daemon=True)
    task.start()

    # tk_app = TkApp(game)
    # tk_app.mainloop()

    task.join()


if __name__ == "__main__":
    _main()
