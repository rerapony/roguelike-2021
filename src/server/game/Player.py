from src.server.game.Character import Character
from src.server.game.map import GameMap


class Player(Character):
    def __init__(self, game_map: GameMap = None, x_coord: int = 0, y_coord: int = 0, blocks_movement: bool = False):
        super().__init__(game_map, x_coord, y_coord, blocks_movement)

    def __str__(self):
        return '@'

    def use(self, item):
        pass

    def pick_up(self, item):
        pass
