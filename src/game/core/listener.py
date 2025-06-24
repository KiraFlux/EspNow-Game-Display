from typing import Callable
from typing import Optional

from game.core.protocol import Player
from serialcmd.serializers import u16
from serialcmd.serializers import u8
from serialcmd.streams.abc import Stream


class GameListener:
    def __init__(self, log: Callable[[str], None]) -> None:
        self.mac: Optional[bytes] = None
        self.players = dict[bytes, Player]()
        self.board = dict[tuple[int, int], int]()
        self.log = log

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

        print(self.mac.hex('-', 2))

        return

    def readLog(self, stream: Stream):
        msg = stream.read(128).rstrip(b'\x00')

        try:
            self.log(f"LOG: {msg.decode()}")

        except UnicodeDecodeError as e:
            self.log(f"{e}: {msg.hex(sep='-', bytes_per_sep=2)}")

        return

    def readBoardStateUpdate(self, stream: Stream):
        self.board.clear()

        length = u16.read(stream)

        for _ in range(length):
            x = u8.read(stream)
            y = u8.read(stream)
            team = u8.read(stream)
            self.board[(x, y)] = team

        return

    def readPlayerListUpdate(self, stream: Stream):
        self.players.clear()

        length = u16.read(stream)

        for _ in range(length):
            mac = stream.read(6)
            username = stream.read(32).rstrip(b'\x00').decode()
            team = u8.read(stream)
            self.players[mac] = Player(username, team)

        return

    def run(self, stream: Stream) -> None:
        while True:
            handler = self.jt.get(u8.read(stream))

            if handler is not None:
                handler.__call__(stream)
