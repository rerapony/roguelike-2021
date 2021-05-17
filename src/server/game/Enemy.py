from typing import Type

from src.server.game.AIController import BaseAI, HostileAI, PassiveAI
from src.server.game.Character import Character
from src.server.game.Components import AttackComponent, HealthComponent
from src.server.game.map.GameMap import GameMap


class Enemy(Character):
    def __init__(self, game_map: GameMap = None,
                 x_coord: int = 0,
                 y_coord: int = 0,
                 vision_radius: float = 10,
                 attack_component: AttackComponent = None,
                 health_component: HealthComponent = None,
                 ai_controller: BaseAI = None):
        super().__init__(game_map, x_coord, y_coord, attack_component=attack_component,
                         health_component=health_component)

        self.death_message = f"{self.name} is dead!"

        self.ai = ai_controller
        self.ai.entity_id = self.entity_id

    @property
    def is_alive(self) -> bool:
        return bool(self.ai)

    def __str__(self):
        return 'E'

    def drop(self):
        pass


class Orc(Enemy):
    def __init__(self, game_map: GameMap = None, x_coord: int = 0, y_coord: int = 0,
                 health: int = 150, attack: int = 10, defense: int = 5, vision_radius: float = 10):
        health_component = HealthComponent(health)
        attack_component = AttackComponent(health_component, defense, attack)
        ai = HostileAI(vision_radius)

        super().__init__(game_map=game_map, x_coord=x_coord, y_coord=y_coord,
                         ai_controller=ai, health_component=health_component, attack_component=attack_component)

    def __str__(self):
        return 'O'

    @property
    def name(self):
        return "Orc"


class Elf(Enemy):
    def __init__(self, game_map: GameMap = None, x_coord: int = 0, y_coord: int = 0,
                 health: int = 150, attack: int = 10, defense: int = 5):
        health_component = HealthComponent(health)
        attack_component = AttackComponent(health_component, defense, attack)
        ai = PassiveAI()

        super().__init__(game_map=game_map, x_coord=x_coord, y_coord=y_coord,
                         ai_controller=ai, health_component=health_component, attack_component=attack_component)

    def __str__(self):
        return 'E'

    @property
    def name(self):
        return "Elf"
