from dpg_ui.core.custom import CustomWidget
from dpg_ui.impl.boxes import IntDisplay
from dpg_ui.impl.boxes import IntInput
from dpg_ui.impl.boxes import TextInput
from dpg_ui.impl.button import Button
from dpg_ui.impl.container.window import ChildWindow
from dpg_ui.impl.text import Text
from game.core.entities.player import Player
from game.core.entities.player import PlayerRegistry
from game.res import Assets
from rs.color import Color


class PlayerCard(CustomWidget):
    """Карточка игрока"""

    def __init__(self, player: Player, player_registry: PlayerRegistry):
        player.addObserver(self._update)
        self.username = TextInput("Игрок", player.rename, default=player.username)
        self.team = IntInput("Команда", default=player.team)
        self.mac = Text(f"MAC: {player.mac}", color=Color.gray(0.75))
        self.score = IntDisplay("Счёт", player.score)

        def _remove():
            player_registry.unregister(player.mac)
            self.delete()

        base = (
            ChildWindow(
                height=180,
                scrollable_y=False,
            )
            .add(self.mac)
            .add(self.username)
            .add(self.team)
            .add(self.score)
            .add(Button("Исключить", _remove))
        )

        super().__init__(base)

    def _update(self, value: Player) -> None:
        self.username.setValue(value.username)
        self.team.setValue(value.team)
        self.score.setValue(value.score)


class PlayerList(CustomWidget):
    """Список игроков"""

    def __init__(self, player_registry: PlayerRegistry) -> None:
        player_registry.addObserver(
            lambda player: self.player_list.add(PlayerCard(player, player_registry))
        )

        self.player_list = ChildWindow()

        base = (
            ChildWindow(
                width=400,
                resizable_x=True,
                background=True
            )
            .add(Text("Игроки").withFont(Assets.label_font))
            .add(self.player_list)
        )

        super().__init__(base)
