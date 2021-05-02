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


class Movement(Command):
    def __init__(self, dx: int, dy: int, entity_id: str):
        super().__init__(entity_id)
        self.dx = dx
        self.dy = dy

    def invoke(self, engine: Engine, entity: MovableEntity) -> None:
        new_x = entity.x + self.dx
        new_y = entity.y + self.dy
        if not engine.game_map.in_bounds(new_x, new_y):
            return
        if not engine.game_map.tiles["walkable"][new_x, new_y]:
            return
        entity.move(self.dx, self.dy)
