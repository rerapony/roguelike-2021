from typing import Tuple, Optional

from src.server.game.Engine import Engine
from src.server.game.Entity import Entity


class Command:
    def __init__(self, engine: Engine, entity_id: str):
        self.engine = engine
        self.entity_id = entity_id
        self.entity = self.engine.game_map.entities[entity_id]

    def invoke(self) -> None:
        raise NotImplementedError()


class Escape(Command):
    def invoke(self) -> None:
        raise SystemExit()


class DirectionCommand(Command):
    def __init__(self, engine: Engine, entity_id: str, dx: int, dy: int):
        super().__init__(engine, entity_id)
        self.dx = dx
        self.dy = dy

    @property
    def dest_xy(self) -> Tuple[int, int]:
        return self.entity.x + self.dx, self.entity.y + self.dy

    @property
    def blocking_entity(self) -> Optional[Entity]:
        return self.engine.game_map.get_blocking_entity(*self.dest_xy)

    def invoke(self) -> None:
        raise NotImplementedError()


class Attack(DirectionCommand):
    def invoke(self) -> None:
        target = self.blocking_entity
        if not target:
            return

        print("Attacking enemy")


class Movement(DirectionCommand):
    def invoke(self) -> None:
        dest_x, dest_y = self.dest_xy

        if not self.engine.game_map.in_bounds(dest_x, dest_y):
            return
        if not self.engine.game_map.tiles["walkable"][dest_x, dest_y]:
            return
        if self.engine.game_map.get_blocking_entity(dest_x, dest_y):
            return

        self.entity.move(self.dx, self.dy)


class Advance(DirectionCommand):
    def invoke(self) -> None:

        if self.blocking_entity:
            return Attack(self.engine, self.entity.entity_id, self.dx, self.dy).invoke()

        else:
            return Movement(self.engine, self.entity_id, self.dx, self.dy).invoke()
