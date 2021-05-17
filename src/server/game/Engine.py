from tcod.console import Console
from tcod.context import Context

from src.client import UI
from src.client.UI import MessageLog


class Engine:
    def __init__(self):
        self.game_map = None
        self.players = []
        self.message_log = MessageLog()

    def handle_enemy_turn(self) -> None:
        for entity in self.game_map.entities.values():
            if entity.entity_id not in self.players:
                if entity.ai:
                    entity.ai.invoke(self)

    def handle_action(self, action) -> None:
        if action is not None:
            print(f"Performing {action}")
            action.invoke(self)

    def render(self, console: Console, context: Context, player_id: str) -> None:
        self.game_map.render(console)
        self.message_log.render(console=console, x=40, y=self.game_map.height - 10, width=40, height=5)
        self.render_hud(console, player_id)
        context.present(console)
        console.clear()

    def render_hud(self, console: Console, player_id: str):
        if player_id in self.players:
            player = self.game_map.entities[player_id]
            self.render_bar(console,
                            player.health_component.health,
                            player.health_component.max_health,
                            total_width=20)

    def render_bar(self,
                   console: Console, current_value: int, maximum_value: int, total_width: int
                   ) -> None:
        bar_width = int(float(current_value) / maximum_value * total_width)

        console.draw_rect(x=5, y=self.game_map.height - 5, width=20, height=1, ch=1, bg=UI.Color.bar_empty)

        if bar_width > 0:
            console.draw_rect(
                x=5, y=self.game_map.height - 5, width=bar_width, height=1, ch=1, bg=UI.Color.bar_filled
            )

        console.print(
            x=5, y=self.game_map.height - 5, string=f"HP: {current_value}/{maximum_value}", fg=UI.Color.bar_text
        )

    def update_fov(self):
        pass
