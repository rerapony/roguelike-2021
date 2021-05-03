from src.server.game.Character import Character


class Enemy(Character):
    def __str__(self):
        return 'E'

    def drop(self):
        pass


class Orc(Enemy):
    def __init__(self, x_coord: int, y_coord: int):
        super().__init__(x_coord, y_coord)
        self.health = 150

    def __str__(self):
        return 'O'
