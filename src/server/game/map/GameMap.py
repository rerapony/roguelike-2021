import random
from typing import Dict

import numpy as np
from tcod.console import Console

from src.server.game.Engine import Engine
from src.server.game.map.tiles import wall


class GameMap:
    def __init__(self, engine: Engine, width: int, height: int, entities: Dict):
        self.engine = engine
        self.width, self.height = width, height
        self.entities = entities
        self.tiles = np.full((width, height), fill_value=wall, order="F")

    def get_blocking_entity(self, location_x: int, location_y: int):
        for entity in self.entities.values():
            if entity.blocks_movement and entity.x == location_x and entity.y == location_y:
                return entity
        return None

    def in_bounds(self, x: int, y: int) -> bool:
        return 0 <= x < self.width and 0 <= y < self.height

    def rand_coord(self) -> (int, int):
        while True:
            x = random.randint(0, self.width - 1)
            y = random.randint(0, self.height - 1)

            if self.tiles["walkable"][x, y]:
                return x, y

    def render(self, console: Console) -> None:
        console.tiles_rgb[0:self.width, 0:self.height] = self.tiles["dark"]
        for entity in self.entities.values():
            console.print(entity.x, entity.y, str(entity))
