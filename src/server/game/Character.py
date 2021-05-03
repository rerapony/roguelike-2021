from src.server.game.Entity import MovableEntity


class Character(MovableEntity):
    def __init__(self, x_coord: int, y_coord: int, is_player: bool = False):
        super().__init__(x_coord, y_coord, is_player)
        self.health = 100
        self.weapon = None
        self.items = []

    def attack(self, damage_receiver):
        pass

    def take_damage(self, damage_causer, damage: float):
        pass
