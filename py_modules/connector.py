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
        data_bytes = bytearray()
        data_dict = ''
        if action == 0:
            length = int.from_bytes(self.client_socket.recv(4), "little")
            while len(data_bytes) < length:
                packet = self.client_socket.recv(length - len(data_bytes))
                data_bytes.extend(packet)
        else:
            return None
        data = data_bytes.decode('utf-8')
        if data != '':
            data_dict = json.loads(data)
        return data_dict

    def get_map(self):

        login_info = self.send_message(1, '{"name":"User7"}')
        player_info = self.send_message(6, '')
        game_info = self.send_message(7, '')
        first_layer_info = self.send_message(10, '{"layer":0}')
        second_layer_info = self.send_message(10, '{"layer":1}')

        return player_info, first_layer_info, second_layer_info

    def get_info(self):
        turn_message = self.send_message(5, '')
        game_info = self.send_message(10, '{"layer":1}')
        return game_info

    def move_train(self, line_idx, speed, train_idx):
        message = '{"line_idx":%d,"speed":%d,"train_idx":%d}' % (line_idx, speed, train_idx)
        move = self.send_message(3, message)

    def upgrade(self):
        message = '{"posts":[],"trains":[1]}' #% (line_idx, speed, train_idx)
        self.send_message(4, message)

    def close_conn(self):
        self.client_socket.close()
