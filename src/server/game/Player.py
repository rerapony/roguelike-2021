from src.server.game.Character import Character


class Player(Character):
    def __init__(self, x_coord: int, y_coord: int):
        super().__init__(x_coord, y_coord, is_player=True)

    def __str__(self):
        return '@'

    def use(self, item):
        pass

    def pick_up(self, item):
        pass
