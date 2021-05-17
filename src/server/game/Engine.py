from tcod.console import Console
from tcod.context import Context


class UI:
    white = (0xFF, 0xFF, 0xFF)
    black = (0x0, 0x0, 0x0)

    player_atk = (0xE0, 0xE0, 0xE0)
    enemy_atk = (0xFF, 0xC0, 0xC0)

    player_die = (0xFF, 0x30, 0x30)
    enemy_die = (0xFF, 0xA0, 0x30)

    welcome_text = (0x20, 0xA0, 0xFF)

    bar_text = white
    bar_filled = (0x0, 0x60, 0x0)
    bar_empty = (0x40, 0x10, 0x10)


class Engine:
    def __init__(self):
        self.game_map = None
        self.players = []

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

        console.draw_rect(x=5, y=self.game_map.height - 5, width=20, height=1, ch=1, bg=UI.bar_empty)

        if bar_width > 0:
            console.draw_rect(
                x=5, y=self.game_map.height - 5, width=bar_width, height=1, ch=1, bg=UI.bar_filled
            )

        console.print(
            x=5, y=self.game_map.height - 5, string=f"HP: {current_value}/{maximum_value}", fg=UI.bar_text
        )

    def update_fov(self):
        pass
