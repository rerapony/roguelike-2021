from tcod.console import Console
from tcod.context import Context


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

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)
        context.present(console)
        console.clear()

    def update_fov(self):
        pass
