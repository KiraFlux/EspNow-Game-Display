from dataclasses import dataclass
from threading import Thread
from typing import Optional

from serialcmd.serializers import u16
from serialcmd.serializers import u8
from serialcmd.streams.abc import Stream
from serialcmd.streams.serials import Serial


def log(s: str):
    print(s)


@dataclass
class Player:
    username: str
    team: int


class GameListener:
    def __init__(self) -> None:
        self.mac: Optional[bytes] = None
        self.players = dict[bytes, Player]()
        self.board = dict[tuple[int, int], int]()

        SendMac = 0x01
        LogOutput = 0x02
        BoardStateUpdate = 0x03
        PlayerListUpdate = 0x04

        self.jt = {
            SendMac: self.readMac,
            LogOutput: self.readLog,
            BoardStateUpdate: self.readBoardStateUpdate,
            PlayerListUpdate: self.readPlayerListUpdate,
        }

    def readMac(self, stream: Stream):
        self.mac = stream.read(6)

        return

    def readLog(self, stream: Stream):
        msg = stream.read(128)

        msg = msg.rstrip(b'\x00')

        try:
            log(f"LOG: {msg.decode()}")

        except UnicodeDecodeError as e:
            log(f"{e}: {msg.hex(sep=b'-', bytes_per_sep=2)}")

        return

    def readBoardStateUpdate(self, stream: Stream):
        length = u16.read(stream)

        for _ in range(length):
            x = u8.read(stream)
            y = u8.read(stream)
            team = u8.read(stream)

            self.board[(x, y)] = team

        return

    def readPlayerListUpdate(self, stream: Stream):
        length = u16.read(stream)

        for _ in range(length):
            mac = stream.read(6)
            username = stream.read(16).rstrip(b'\x00').decode()
            team = u8.read(stream)

            self.players[mac] = Player(username, team)

        return

    def run(self, stream: Stream) -> None:
        try:
            while True:
                opp = u8.read(stream)

                foo = self.jt.get(opp)

                if foo is not None:
                    foo.__call__(stream)

        except KeyboardInterrupt:
            return


def _main():
    p = Serial("COM8", 115200)
    listener = GameListener()

    task = Thread(target=listener.run, args=(p,))
    task.start()

    task.join()


_main()
