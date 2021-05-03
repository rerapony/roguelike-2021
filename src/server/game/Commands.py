from src.server.game.Engine import Engine
from src.server.game.Entity import MovableEntity, Entity


class Command:
    def __init__(self, entity_id):
        self.entity_id = entity_id

    def invoke(self, engine: Engine, entity: Entity) -> None:
        raise NotImplementedError()


class Escape(Command):
    def invoke(self, engine: Engine, entity: Entity) -> None:
        raise SystemExit()


class DirectionCommand(Command):
    def __init__(self, dx: int, dy: int, entity_id: str):
        super().__init__(entity_id)
        self.dx = dx
        self.dy = dy

    def invoke(self, engine: Engine, entity: Entity) -> None:
        raise NotImplementedError()


class Attack(DirectionCommand):
    def invoke(self, engine: Engine, entity: Entity) -> None:
        new_x = entity.x + self.dx
        new_y = entity.y + self.dy
        target = engine.game_map.get_blocking_entity(new_x, new_y)
        if not target:
            return

        print("Attacking enemy")


class Movement(DirectionCommand):
    def invoke(self, engine: Engine, entity: MovableEntity) -> None:
        new_x = entity.x + self.dx
        new_y = entity.y + self.dy
        if not engine.game_map.in_bounds(new_x, new_y):
            return
        if not engine.game_map.tiles["walkable"][new_x, new_y]:
            return
        if engine.game_map.get_blocking_entity(new_x, new_y):
            return

        entity.move(self.dx, self.dy)


class Advance(DirectionCommand):
    def invoke(self, engine: Engine, entity: MovableEntity) -> None:
        new_x = entity.x + self.dx
        new_y = entity.y + self.dy

        if engine.game_map.get_blocking_entity(new_x, new_y):
            return Attack(self.dx, self.dy, entity.entity_id).invoke(engine, entity)

        else:
            return Movement(self.dx, self.dy, entity.entity_id).invoke(engine, entity)
