from src.server.game.Components import AttackComponent, HealthComponent
from src.server.game.Engine import Engine
from src.server.game.Entity import MovableEntity
from src.server.game.map.GameMap import GameMap


class Character(MovableEntity):
    def __init__(self,
                 game_map: GameMap = None,
                 x_coord: int = 0,
                 y_coord: int = 0,
                 attack_component: AttackComponent = None,
                 health_component: HealthComponent = None):
        super().__init__(game_map, x_coord, y_coord, blocks_movement=True)

        self.death_message = None

        self.health_component = health_component
        self.health_component.entity_id = self.entity_id

        self.attack_component = attack_component
        self.attack_component.entity_id = self.entity_id

    def die(self, engine: Engine) -> None:
        engine.message_log.add_message(
           self.death_message
        )

        del engine.game_map.entities[self.entity_id]
