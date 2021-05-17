from src.server.game.Engine import Engine

import numpy as np


class BaseComponent:
    def __init__(self):
        self.entity_id = None

    def entity(self, engine: Engine):
        return engine.game_map.entities[self.entity_id]


class HealthComponent(BaseComponent):
    def __init__(self, max_health: int):
        super().__init__()
        self.health = max_health
        self.max_health = max_health

    @property
    def value(self):
        return self.health

    @value.setter
    def value(self, new_value: int):
        self.health = np.clip(new_value, 0, self.max_health)


class AttackComponent(BaseComponent):
    def __init__(self, health: HealthComponent, defense: int, attack: int):
        super().__init__()
        self.defense = defense
        self.attack = attack
        self.health_component = health

    def take_damage(self, engine: Engine, damage: float):
        true_damage = damage - self.defense
        entity = self.entity(engine)

        if true_damage > 0:
            engine.message_log.add_message(
                f"{entity.name} takes {true_damage} damage!"
            )

            self.health_component.value -= true_damage

            engine.message_log.add_message(
                f"{entity.name} HP is: {self.health_component.value} damage!"
            )

        if self.health_component.value <= 0:
            entity.die(engine)
