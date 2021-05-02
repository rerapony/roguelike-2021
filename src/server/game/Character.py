from src.server.game.Entity import MovableEntity


class Character(MovableEntity):
    def __init__(self, x_coord: int, y_coord: int):
        super().__init__(x_coord, y_coord)
        self.health = 100
        self.weapon = None
        self.items = []

    def attack(self, damage_receiver):
        pass

    def take_damage(self, damage_causer, damage: float):
        pass
