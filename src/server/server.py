import pickle
import socket
import threading
import asyncio
import queue
from typing import Set

from src.server.game.Engine import Engine
from src.server.game.Player import Player
from src.server.game.map.DungeonGenerator import generate_dungeon


class Server:
    def __init__(self, host=None, port=None):
        self.HOST = host or '127.0.0.1'
        self.PORT = port or 5050
        self.FORMAT = 'utf-8'
        self.HEADER = 64
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.socket.bind((self.HOST, self.PORT))
        self.action_queue = queue.Queue()
        self.players: Set = set()
        self.game = None

    def send(self, conn, msg):
        message = pickle.dumps(msg)
        msg_length = len(message)
        send_length = str(msg_length).encode(self.FORMAT)
        send_length += b' ' * (self.HEADER - len(send_length))
        conn.send(send_length)
        conn.send(message)

    def receive(self, conn):
        msg_length = conn.recv(self.HEADER).decode(self.FORMAT)
        if not msg_length:
            return
        msg_length = int(msg_length)
        data_binary = conn.recv(msg_length)
        data = pickle.loads(data_binary)
        return data

    def handle_player(self):
        print("handle player")
        conn, addr = self.socket.accept()
        with conn:
            print('Connected by', addr)
            self.players.add(conn)
            coords = self.game.game_map.rand_coord()
            player = Player(coords[0], coords[1])
            self.game.entities[player.entity_id] = player
            self.send(conn, (self.game, player.entity_id))
            while True:
                action = self.receive(conn)
                print("Got action {}".format(action))
                self.action_queue.put(action)

    def init_game(self):
        map = generate_dungeon(20, 15, 20, 100, 100)
        self.game = Engine({}, map)

    async def start(self):
        print("Server started on port: {}".format(self.PORT))
        self.init_game()
        with self.socket as s:
            s.listen()
            connection_thread = threading.Thread(target=self.handle_player, args=())
            connection_thread.start()
            while True:
                await asyncio.sleep(0)
                action = self.action_queue.get()
                if action is not None:
                    self.game.handle_action(action)
                for player in self.players:
                    self.send(player, self.game)


if __name__ == "__main__":
    server = Server()
    asyncio.run(server.start())
