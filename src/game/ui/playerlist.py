from dpg_ui.core.custom import CustomWidget
from dpg_ui.impl.boxes import DisplayInt
from dpg_ui.impl.boxes import InputText
from dpg_ui.impl.buttons import Button
from dpg_ui.impl.containers import ChildWindow
from dpg_ui.impl.text import Text
from game.core.entities.player import Player
from game.core.entities.player import PlayerRegistry
from rs.color import Color


class PlayerCard(CustomWidget):
    """Карточка игрока"""

    def __init__(self, player: Player, player_registry: PlayerRegistry):
        player.addObserver(self._update)
        self.username = InputText("Игрок", player.rename, default=player.username)
        self.team = Text(player.team.name, color=player.team.color, bullet=True)
        self.mac = Text(f"MAC: {player.mac}", color=Color.gray(0.75))
        self.score = DisplayInt("Счёт", player.score)

        def _remove():
            player_registry.unregister(player.mac)
            self.delete()

        base = (
            ChildWindow(
                _height=180,
            )
            .add(self.mac)
            .add(self.username)
            .add(self.team)
            .add(self.score)
            .add(Button("Исключить", _on_click=_remove))
        )

        super().__init__(base)

    def _update(self, p: Player) -> None:
        self.username.setValue(p.username)
        self.team.setValue(p.team.name)
        self.team.setColor(p.team.color)
        self.score.setValue(p.score)


class PlayerList(CustomWidget):
    """Список игроков"""

    def __init__(self, player_registry: PlayerRegistry) -> None:
        player_list = ChildWindow()

        player_registry.addObserver(
            lambda player: player_list.add(PlayerCard(player, player_registry))
        )

        super().__init__(player_list)
