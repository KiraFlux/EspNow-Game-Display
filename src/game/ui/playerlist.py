from dpg_ui.core.custom import CustomWidget
from dpg_ui.impl.boxes import DisplayInt
from dpg_ui.impl.boxes import InputText
from dpg_ui.impl.buttons import Button
from dpg_ui.impl.containers import ChildWindow
from dpg_ui.impl.text import Text
from game.core.entities.player import Player
from game.core.entities.player import PlayerRegistry
from rs.misc.color import Color


class PlayerCard(CustomWidget):
    """Карточка игрока"""

    def __init__(self, player: Player, player_registry: PlayerRegistry):
        player.addObserver(self._update)

        self._username = InputText("Игрок", default=player.username).withHandler(player.rename)
        self._team = Text(player.team.name, color=player.team.color, bullet=True)
        self._mac = Text(f"MAC: {player.mac}", color=Color.gray(0.75))
        self._score = DisplayInt("Счёт", default=player.score)

        base = (
            ChildWindow(
                _height=180,
            )
            .add(self._mac)
            .add(self._username)
            .add(self._team)
            .add(self._score)
            .add(
                Button()
                .withLabel("Исключить")
                .withHandler(self.delete)
            )
        )

        super().__init__(base)

        self.attachDeleteObserver(lambda _: player_registry.unregister(player.mac))

    def _update(self, p: Player) -> None:
        self._username.setValue(p.username)
        self._team.setValue(p.team.name)
        self._team.setColor(p.team.color)
        self._score.setValue(p.score)


class PlayerList(CustomWidget):
    """Список игроков"""

    def __init__(self, player_registry: PlayerRegistry) -> None:
        player_list = ChildWindow()

        player_registry.addObserver(
            lambda player: player_list.add(PlayerCard(player, player_registry))
        )

        super().__init__(player_list)
