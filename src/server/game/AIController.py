import random
from typing import List, Tuple

import numpy as np
import tcod

from src.server.game.Commands import Command, Attack, Advance, Wait
from src.server.game.Components import BaseComponent
from src.server.game.Engine import Engine


class BaseAI(BaseComponent):
    def invoke(self, engine: Engine) -> None:
        raise NotImplementedError()

    def get_path_to(self, engine: Engine, dest_x: int, dest_y: int) -> List[Tuple[int, int]]:
        cost = np.array(engine.game_map.tiles["walkable"], dtype=np.int8)

        for entity in engine.game_map.entities.values():
            if entity.blocks_movement and cost[entity.x, entity.y]:
                cost[entity.x, entity.y] += 10

        graph = tcod.path.SimpleGraph(cost=cost, cardinal=2, diagonal=3)
        pathfinder = tcod.path.Pathfinder(graph)

        pathfinder.add_root((self.entity(engine).x, self.entity(engine).y))  # Start position.

        path: List[List[int]] = pathfinder.path_to((dest_x, dest_y))[1:].tolist()

        return [(index[0], index[1]) for index in path]


class PassiveAI(BaseAI):
    def __init__(self):
        super().__init__()

    def invoke(self, engine: Engine) -> None:
        return Wait(self.entity_id).invoke(engine)


class HostileAI(BaseAI):
    def __init__(self, vision_radius: float):
        super().__init__()
        self.path: List[Tuple[int, int]] = []
        self.target_id = None
        self.vision_radius = vision_radius

    def target(self, engine: Engine):
        if self.target_id is None:
            self.target_id = random.randint(0, len(engine.players) - 1)

        return engine.game_map.entities[engine.players[self.target_id]]

    def invoke(self, engine: Engine) -> None:

        dx = self.target(engine).x - self.entity(engine).x
        dy = self.target(engine).y - self.entity(engine).y

        distance = max(abs(dx), abs(dy))  # Chebyshev distance.

        if distance <= 1:
            return Attack(self.entity_id, dx, dy).invoke(engine)

        if distance <= self.vision_radius:
            self.path = self.get_path_to(engine, self.target(engine).x, self.target(engine).y)

            if self.path:
                dest_x, dest_y = self.path.pop(0)
                return Advance(
                    self.entity_id,
                    dest_x - self.entity(engine).x,
                    dest_y - self.entity(engine).y,
                ).invoke(engine)

        return Wait(self.entity_id).invoke(engine)
