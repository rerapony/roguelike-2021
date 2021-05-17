from typing import List, Reversible, Tuple
import textwrap

import tcod


class Color:
    white = (0xFF, 0xFF, 0xFF)
    black = (0x0, 0x0, 0x0)

    player_atk = (0xE0, 0xE0, 0xE0)
    enemy_atk = (0xFF, 0xC0, 0xC0)

    player_die = (0xFF, 0x30, 0x30)
    enemy_die = (0xFF, 0xA0, 0x30)

    welcome_text = (0x20, 0xA0, 0xFF)

    bar_text = white
    bar_filled = (0x0, 0x60, 0x0)
    bar_empty = (0x40, 0x10, 0x10)


class Message:
    def __init__(self, text: str, fg: Tuple[int, int, int]):
        self.plain_text = text
        self.fg = fg
        self.count = 1

    @property
    def full_text(self) -> str:
        if self.count > 1:
            return f"{self.plain_text} (x{self.count})"
        return self.plain_text


class MessageLog:
    def __init__(self) -> None:
        self.messages: List[Message] = []

    def add_message(
            self, text: str, fg: Tuple[int, int, int] = Color.white, *, stack: bool = True,
    ) -> None:
        if stack and self.messages and text == self.messages[-1].plain_text:
            self.messages[-1].count += 1
        else:
            self.messages.append(Message(text, fg))

    def render(
            self, console: tcod.Console, x: int, y: int, width: int, height: int,
    ) -> None:
        self.render_messages(console, x, y, width, height, self.messages)

    @staticmethod
    def render_messages(
            console: tcod.Console,
            x: int,
            y: int,
            width: int,
            height: int,
            messages: Reversible[Message],
    ) -> None:
        y_offset = height - 1

        for message in reversed(messages):
            for line in reversed(textwrap.wrap(message.full_text, width)):
                console.print(x=x, y=y + y_offset, string=line, fg=message.fg)
                y_offset -= 1
                if y_offset < 0:
                    return  # No more space to print messages.
