from dpg_ui.core.custom import CustomWidget
from dpg_ui.impl.boxes import IntDisplay
from dpg_ui.impl.boxes import IntInput
from dpg_ui.impl.boxes import TextInput
from dpg_ui.impl.container.window import ChildWindow
from dpg_ui.impl.text import Text
from game.core.entities.player import Player
from game.core.entities.player import PlayerRegistry
from misc.observer import Observer
from rs.color import Color


class PlayerCard(CustomWidget, Observer[Player]):
    """Карточка игрока"""

    def __init__(self, player: Player):
        player.addObserver(self)
        self.username = TextInput("Игрок", player.rename, default=player.username)
        self.team = IntInput(label="Команда", _interval_min=0, _value_default=player.team)
        self.mac = Text(_value_default=f"MAC: {player.mac}", _color=Color.gray(0.7))
        self.score = IntDisplay(_value_default=player.score, label="Счёт")

        base = (
            ChildWindow(
                height=150,
                scrollable_y=False,
            )
            .add(self.mac)
            .add(self.username)
            .add(self.team)
            .add(self.score)
        )

        super().__init__(base)

    def update(self, value: Player) -> None:
        self.username.setValue(value.username)
        self.team.setValue(value.team)
        self.score.setValue(value.score)


class PlayerList(CustomWidget, Observer[Player]):
    """Список игроков"""

    def __init__(self, player_registry: PlayerRegistry) -> None:
        player_registry.addObserver(self)

        self.player_list = ChildWindow()

        base = (
            ChildWindow(
                width=400,
                resizable_x=True,
                background=True
            )
            .add(Text(_value_default="ИГРОКИ"))
            .add(self.player_list)
        )

        super().__init__(base)

    def update(self, value: Player) -> None:
        self.player_list.add(PlayerCard(value))
