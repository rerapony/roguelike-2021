import pickle
import socket

import tcod

from src.client.InputHandler import InputHandler


class Client:
    def __init__(self, server=None, port=None):
        self.screen_size = (70, 70)
        self.SERVER = server or "127.0.0.1"
        self.PORT = port or 5050
        self.FORMAT = 'utf-8'
        self.HEADER = 64
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client.connect((self.SERVER, self.PORT))

    def send(self, msg):
        message = pickle.dumps(msg)
        msg_length = message.__sizeof__()
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        self.client.send(send_length)
        self.client.send(message)

    def receive(self):
        msg_length = self.client.recv(self.HEADER).decode(self.FORMAT)
        msg_length = int(msg_length)
        data_binary = self.client.recv(msg_length)
        while len(data_binary) < msg_length:
            data_binary += self.client.recv(msg_length - len(data_binary))
        data = pickle.loads(data_binary)
        return data

    def click_handler(self, event):
        if event.event_type == "down":
            self.send(event.name)

    def start(self):
        screen_width = self.screen_size[0]
        screen_height = self.screen_size[1]

        engine, player_id = self.receive()
        with tcod.context.new_terminal(
                screen_width,
                screen_height
        ) as context:
            input_handler = InputHandler(player_id)
            root_console = tcod.Console(engine.game_map.width, engine.game_map.height, order="F")
            while True:
                engine.render(console=root_console, context=context)
                for event in tcod.event.wait():
                    action = input_handler.dispatch(event)
                    if action is not None:
                        self.send(action)
                        engine = self.receive()


if __name__ == "__main__":
    client = Client()
    client.start()
