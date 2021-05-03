import copy
import random

from src.server.game.map.GameMap import GameMap


class Entity:
    def __init__(self, x_coord: int, y_coord: int, is_player: bool = False, blocks_movement: bool = False):
        self.x = x_coord
        self.y = y_coord
        self.entity_id = self.generate_id()
        self.blocks_movement = blocks_movement
        self.is_player = is_player

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
        game_map.entities[clone.entity_id] = clone
        return clone


class MovableEntity(Entity):
    def __init__(self, x_coord: int, y_coord: int, is_player: bool = False):
        super().__init__(x_coord, y_coord, is_player)

    def move(self, dx: int, dy: int):
        self.x += dx
        self.y += dy
