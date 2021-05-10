import asyncio
import pickle
import queue
import socket
import threading
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
        while len(data_binary) < msg_length:
            print(len(data_binary))
            data_binary += conn.recv(msg_length - len(data_binary))
        data = pickle.loads(data_binary)
        return data

    def handle_player(self):
        print("handle player")
        conn, addr = self.socket.accept()
        with conn:
            print('Connected by', addr)
            self.players.add(conn)
            coords = self.game.game_map.rand_coord()

            player = Player(game_map=self.game.game_map, x_coord=coords[0], y_coord=coords[1], blocks_movement=True)

            self.game.game_map.entities[player.entity_id] = player

            if player.entity_id not in self.game.players:
                self.game.players.append(player.entity_id)

            self.send(conn, (self.game, player.entity_id))
            while True:
                action = self.receive(conn)
                print("Got action {}".format(action))
                self.action_queue.put(action)

    def init_game(self):
        self.game = Engine()

        map = generate_dungeon(max_rooms=20, room_min_size=15, room_max_size=20, map_width=100,
                               map_height=100, max_num_of_enemies=3, engine=self.game)
        self.game.game_map = map
        self.game.update_fov()

    async def start(self):
        print("Server started on port: {}".format(self.PORT))
        self.init_game()
        with self.socket as s:
            s.listen()
            connection_thread = threading.Thread(target=self.handle_player, args=())
            connection_thread.start()
            while True:
                await asyncio.sleep(0)
                print("Queue")
                action = self.action_queue.get()
                if action is not None:
                    print("Game")
                    self.game.handle_action(action)
                    self.game.handle_enemy_turn()
                for player in self.players:
                    self.send(player, self.game)


if __name__ == "__main__":
    server = Server()
    asyncio.run(server.start())
