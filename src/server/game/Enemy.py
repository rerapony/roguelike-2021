from typing import Type

from src.server.game.AIController import BaseAI, HostileAI
from src.server.game.Character import Character
from src.server.game.Components import AttackComponent
from src.server.game.map.GameMap import GameMap


class Enemy(Character):
    def __init__(self, game_map: GameMap = None, x_coord: int = 0, y_coord: int = 0,
                 ai_cls: Type[BaseAI] = None, attack_component: AttackComponent = None):
        super().__init__(game_map, x_coord, y_coord, True)

        self.ai = ai_cls(self.entity_id)

        self.attack_component = attack_component
        self.attack_component.entity_id = self.entity_id

    @property
    def is_alive(self) -> bool:
        return bool(self.ai)

    def __str__(self):
        return 'E'

    def drop(self):
        pass


class Orc(Enemy):
    def __init__(self, game_map: GameMap = None, x_coord: int = 0, y_coord: int = 0):
        self.health = 150
        self.attack = 10
        self.defense = 5

        super().__init__(game_map=game_map, x_coord=x_coord, y_coord=y_coord,
                         ai_cls=HostileAI,
                         attack_component=AttackComponent(self.health, self.defense, self.attack))

        self.attack_component.entity_id = self.entity_id

    def __str__(self):
        return 'O'


class Elf(Enemy):
    def __init__(self, game_map: GameMap = None, x_coord: int = 0, y_coord: int = 0):
        self.health = 150
        self.attack = 10
        self.defense = 5

        super().__init__(game_map=game_map, x_coord=x_coord, y_coord=y_coord,
                         ai_cls=None, attack_component=AttackComponent(self.health, self.defense, self.attack))

        self.attack_component.entity_id = self.entity_id

    def __str__(self):
        return 'E'
