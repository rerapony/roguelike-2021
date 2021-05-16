from typing import Tuple, Optional

from src.server.game.Engine import Engine
from src.server.game.Entity import Entity


class Command:
    def __init__(self, entity_id: str):
        self.entity_id = entity_id

    def entity(self, engine: Engine):
        return engine.game_map.entities[self.entity_id]

    def invoke(self, engine: Engine) -> None:
        raise NotImplementedError()


class Escape(Command):
    def invoke(self, engine: Engine) -> None:
        raise SystemExit()


class Wait(Command):
    def invoke(self, engine: Engine) -> None:
        pass


class DirectionCommand(Command):
    def __init__(self, entity_id: str, dx: int, dy: int):
        super().__init__(entity_id)
        self.dx = dx
        self.dy = dy

    def dest_xy(self, engine: Engine) -> Tuple[int, int]:
        entity = self.entity(engine)
        return entity.x + self.dx, entity.y + self.dy

    def blocking_entity(self, engine: Engine) -> Optional[Entity]:
        return engine.game_map.get_blocking_entity(*self.dest_xy(engine))

    def invoke(self, engine: Engine) -> None:
        raise NotImplementedError()


class Attack(DirectionCommand):
    def invoke(self, engine: Engine) -> None:

        target = self.blocking_entity(engine)
        if not target:
            return  # No entity to attack.

        damage = self.entity(engine).attack_component.attack - target.attack_component.defense

        if damage > 0:
            print(f"{target.name} HP is: {target.attack_component.health}")

            target.attack_component.health -= damage
            target.attack_component.update_hp(engine)
        else:
            print(f"Attack does no damage.")


class Movement(DirectionCommand):
    def invoke(self, engine: Engine) -> None:
        dest_x, dest_y = self.dest_xy(engine)

        if not engine.game_map.in_bounds(dest_x, dest_y):
            return
        if not engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return
        if engine.game_map.get_blocking_entity(dest_x, dest_y):
            return

        self.entity(engine).move(self.dx, self.dy)


class Advance(DirectionCommand):
    def invoke(self, engine: Engine) -> None:

        if self.blocking_entity(engine):
            return Attack(self.entity_id, self.dx, self.dy).invoke(engine)

        else:
            return Movement(self.entity_id, self.dx, self.dy).invoke(engine)
