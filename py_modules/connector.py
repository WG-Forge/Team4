import socket
import json


class Connector:
    def __init__(self):
        self.server_addr = 'wgforge-srv.wargaming.net'
        self.server_port = 443
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((self.server_addr, self.server_port))

    def send_message(self, code, message):

        byte_message = code.to_bytes(4, 'little') + len(message).to_bytes(4, 'little') + bytes(message, 'utf-8')

        self.client_socket.sendall(byte_message)

        action = int.from_bytes(self.client_socket.recv(4), "little")
        # print(message)
        # print(action)
        # print()
        data_bytes = bytearray()
        data_dict = ''
        if action == 0:
            length = int.from_bytes(self.client_socket.recv(4), "little")
            while len(data_bytes) < length:
                packet = self.client_socket.recv(length - len(data_bytes))
                data_bytes.extend(packet)
        # elif action == 4:
        #     return 4
        else:
            # print(message)
            return 4
        data = data_bytes.decode('utf-8')
        if data != '':
            data_dict = json.loads(data)

        return data_dict

    def login(self,  player_name, game_name=None, number=1):
        name = '}'
        if game_name is not None:

            name = ', "game": "%s"}' % game_name

        message = '{"name": "%s", "num_turns": 500, "num_players": %s' % (player_name, number)
        message += name
        login_info = self.send_message(1, message)
        return login_info

    def get_map(self):

        player_info = self.send_message(6, '')

        first_layer_info = self.send_message(10, '{"layer":0}')
        second_layer_info = self.send_message(10, '{"layer":1}')
        ten_layer_info = self.send_message(10, '{"layer":10}')
        # print(self.get_game())

        return player_info, first_layer_info, second_layer_info, ten_layer_info

    def get_game(self):
        return self.send_message(7, '')

    def get_info(self):
        game_info = self.send_message(10, '{"layer":1}')
        return game_info

    def next_turn(self):
        turn_message = self.send_message(5, '')

    def move_train(self, line_idx, speed, train_idx):
        message = '{"line_idx":%d,"speed":%d,"train_idx":%d}' % (line_idx, speed, train_idx)
        move = self.send_message(3, message)

    def upgrade(self, upgrade_dict):
        message = '{"posts":%s,"trains":%s}' % (str(upgrade_dict['posts']), str(upgrade_dict['trains']))
        return self.send_message(4, message)

    def close_conn(self):
        self.client_socket.close()
