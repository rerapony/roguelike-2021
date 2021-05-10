from src.server.game.Character import Character
from src.server.game.map.GameMap import GameMap


class Enemy(Character):
    def __str__(self):
        return 'E'

    def drop(self):
        pass


class Orc(Enemy):
    def __init__(self, game_map: GameMap = None, x_coord: int = 0, y_coord: int = 0, blocks_movement: bool = False):
        super().__init__(game_map, x_coord, y_coord, blocks_movement)
        self.health = 150

    def __str__(self):
        return 'O'


class Elf(Enemy):
    def __init__(self, game_map: GameMap = None, x_coord: int = 0, y_coord: int = 0, blocks_movement: bool = False):
        super().__init__(game_map, x_coord, y_coord, blocks_movement)
        self.health = 150

    def __str__(self):
        return '1'
