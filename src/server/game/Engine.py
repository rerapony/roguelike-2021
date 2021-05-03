from typing import Dict

from tcod.console import Console
from tcod.context import Context

from src.server.game.Entity import Entity, MovableEntity
from src.server.game.map.GameMap import GameMap


class Engine:
    def __init__(self, game_map: GameMap):
        self.game_map = game_map

    def handle_action(self, action) -> None:
        if action is not None:
            print(f"Performing {action}")
            action.invoke(self, self.game_map.entities[action.entity_id])

    def render(self, console: Console, context: Context) -> None:
        self.game_map.render(console)
        context.present(console)
        console.clear()
