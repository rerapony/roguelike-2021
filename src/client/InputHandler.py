from typing import Optional

import tcod.event

from src.server.game.Commands import Command, Escape, Advance


class InputHandler(tcod.event.EventDispatch[Command]):

    def __init__(self, engine, entity_id):
        super().__init__()
        self.engine = engine
        self.entity_id = entity_id

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Command]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Command]:
        action: Optional[Command] = None

        key = event.sym

        if key == tcod.event.K_UP:
            action = Advance(engine=self.engine, entity_id=self.entity_id, dx=0, dy=-1)
        elif key == tcod.event.K_DOWN:
            action = Advance(engine=self.engine, entity_id=self.entity_id, dx=0, dy=-1)
        elif key == tcod.event.K_LEFT:
            action = Advance(engine=self.engine, entity_id=self.entity_id, dx=0, dy=-1)
        elif key == tcod.event.K_RIGHT:
            action = Advance(engine=self.engine, entity_id=self.entity_id, dx=0, dy=-1)

        elif key == tcod.event.K_ESCAPE:
            action = Escape(engine=self.engine, entity_id=self.entity_id)

        return action
