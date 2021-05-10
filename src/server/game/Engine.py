from tcod.console import Console
from tcod.context import Context


class Engine:
    def __init__(self):
        self.game_map = None

    def handle_enemy_turn(self) -> None:
        for entity in self.game_map.entities.values():
            if not entity.is_player:
                print("Enemy turn")

    def handle_action(self, action) -> None:
        if action is not None:
            print(f"Performing {action}")
            action.invoke(self, self.game_map.entities[action.entity_id])

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)
        context.present(console)
        console.clear()

    def update_fov(self):
        pass
