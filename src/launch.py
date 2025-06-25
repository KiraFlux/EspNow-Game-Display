from threading import Thread

from game.core.protocol import GameProtocol
from serialcmd.impl.stream.serials import SerialStream


def _listener_task(listener: GameProtocol):
    print('Senders')
    print('\n'.join(map(str, listener.getSenders())))
    print('Receivers')
    print('\n'.join(map(str, listener.getReceivers())))

    while True:
        result = listener.pull()

        if result.is_err():
            print(f"task pull: {result.err().unwrap()}")


def _main():
    # logs = Queue()

    serial = SerialStream("COM8", 115200)

    listener = GameProtocol(serial)

    task = Thread(target=_listener_task, args=(listener,), daemon=True)
    task.start()

    # tk_app = TkApp(listener, logs)
    # tk_app.mainloop()

    task.join()


if __name__ == "__main__":
    _main()
