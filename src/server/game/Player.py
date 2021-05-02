from src.server.game.Character import Character


class Player(Character):
    def __str__(self):
        return '@'

    def use(self, item):
        pass

    def pick_up(self, item):
        pass
