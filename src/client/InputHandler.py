from typing import Optional

import tcod.event

from src.server.game.Commands import Command, Escape, Advance, Wait

MOVE_KEYS = {
    # Arrow keys.
    tcod.event.K_UP: (0, -1),
    tcod.event.K_DOWN: (0, 1),
    tcod.event.K_LEFT: (-1, 0),
    tcod.event.K_RIGHT: (1, 0),
    tcod.event.K_HOME: (-1, -1),
    tcod.event.K_END: (-1, 1),
    tcod.event.K_PAGEUP: (1, -1),
    tcod.event.K_PAGEDOWN: (1, 1),
    # Numpad keys.
    tcod.event.K_KP_1: (-1, 1),
    tcod.event.K_KP_2: (0, 1),
    tcod.event.K_KP_3: (1, 1),
    tcod.event.K_KP_4: (-1, 0),
    tcod.event.K_KP_6: (1, 0),
    tcod.event.K_KP_7: (-1, -1),
    tcod.event.K_KP_8: (0, -1),
    tcod.event.K_KP_9: (1, -1),
    # Vi keys.
    tcod.event.K_h: (-1, 0),
    tcod.event.K_j: (0, 1),
    tcod.event.K_k: (0, -1),
    tcod.event.K_l: (1, 0),
    tcod.event.K_y: (-1, -1),
    tcod.event.K_u: (1, -1),
    tcod.event.K_b: (-1, 1),
    tcod.event.K_n: (1, 1),
}

WAIT_KEYS = {
    tcod.event.K_PERIOD,
    tcod.event.K_KP_5,
    tcod.event.K_CLEAR,
}


class InputHandler(tcod.event.EventDispatch[Command]):

    def __init__(self, entity_id):
        super().__init__()
        self.entity_id = entity_id

    def ev_quit(self, event: tcod.event.Quit) -> Optional[Command]:
        raise SystemExit()

    def ev_keydown(self, event: tcod.event.KeyDown) -> Optional[Command]:
        action: Optional[Command] = None

        key = event.sym

        if key in MOVE_KEYS:
            dx, dy = MOVE_KEYS[key]
            action = Advance(self.entity_id, dx, dy)

        elif key in WAIT_KEYS:
            action = Wait(self.entity_id)

        elif key == tcod.event.K_ESCAPE:
            action = Escape(self.entity_id)

        return action
