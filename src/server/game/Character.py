from src.server.game.Entity import MovableEntity
from src.server.game.map.GameMap import GameMap


class Character(MovableEntity):
    def __init__(self, game_map: GameMap = None, x_coord: int = 0, y_coord: int = 0, blocks_movement: bool = False):
        super().__init__(game_map, x_coord, y_coord, blocks_movement)
        self.health = 100
        self.weapon = None
        self.items = []

    def attack(self, damage_receiver):
        pass

    def take_damage(self, damage_causer, damage: float):
        pass
