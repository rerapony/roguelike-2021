import copy
import random

from src.server.game.map.GameMap import GameMap


class Entity:
    def __init__(self, game_map: GameMap = None, x_coord: int = 0, y_coord: int = 0, blocks_movement: bool = False):
        self.x = x_coord
        self.y = y_coord
        self.entity_id = self.generate_id()
        self.blocks_movement = blocks_movement
        self.game_map = game_map

        if self.game_map is not None:
            self.game_map.entities[self.entity_id] = self

    @staticmethod
    def generate_id():
        entity_id = ''
        for i in range(0, 7):
            entity_id += random.randint(0, 1000).__str__()
        return entity_id

    def __str__(self):
        return ' '

    @property
    def color(self):
        return tuple([0, 0, 0])

    def spawn(self, game_map: GameMap, x: int, y: int):
        clone = copy.deepcopy(self)
        clone.x = x
        clone.y = y
        clone.game_map = game_map
        clone.game_map.entities[clone.entity_id] = clone
        return clone

    def place(self, game_map: GameMap = None, x: int = 0, y: int = 0) -> None:
        self.x = x
        self.y = y
        if game_map is not None:
            if self.game_map is not None:
                del self.game_map.entities[self.entity_id]
            self.game_map = game_map
            self.game_map.entities[self.entity_id] = self


class MovableEntity(Entity):
    def __init__(self, game_map: GameMap = None, x_coord: int = 0, y_coord: int = 0, blocks_movement: bool = False):
        super().__init__(game_map, x_coord, y_coord, blocks_movement)

    def move(self, dx: int, dy: int):
        self.x += dx
        self.y += dy
