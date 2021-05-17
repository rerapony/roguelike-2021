from src.server.game.Character import Character
from src.server.game.Components import AttackComponent, HealthComponent
from src.server.game.map import GameMap


class Player(Character):
    def __init__(self, game_map: GameMap = None, x_coord: int = 0, y_coord: int = 0,
                 health: int = 300, attack: int = 50, defense: int = 0):

        health_component = HealthComponent(health)
        attack_component = AttackComponent(health_component, defense, attack)

        super().__init__(game_map, x_coord, y_coord, health_component=health_component, attack_component=attack_component)

        self.death_message = "Game over!"

    def __str__(self):
        return '@'

    @property
    def name(self):
        return "MainCharacter"

    def use(self, item):
        pass

    def pick_up(self, item):
        pass
