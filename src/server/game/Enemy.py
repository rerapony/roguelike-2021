from src.server.game.Character import Character


class Enemy(Character):
    def __str__(self):
        return 'E'

    def drop(self):
        pass
