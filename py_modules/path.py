from py_modules.train import Train


class Path:
    def __init__(self, path, length, connector, stop_dict=None):
        self.path = path
        self.length = length
        self.income = 0
        self.connector = connector
        self.current_track = [path[0][0], path[0][1], 0]  # line_id, direction, length
        self.current_track_idx = 0
        self.stop_dict = {} if stop_dict is None else stop_dict  # {point_idx: time}
        self.tick = 0
        self.resume = False

    def copy(self):
        return Path(self.path, self.length, self.connector, stop_dict=self.stop_dict)

    def should_stop(self, train_idx):
        if self.tick in self.stop_dict and self.stop_dict[self.tick] > 0:
            self.connector.move_train(self.current_track[0], 0, train_idx)
            self.stop_dict[self.tick] -= 1
            if self.stop_dict[self.tick] == 0:
                del self.stop_dict[self.tick]
                self.resume = True
            return True
        return False

    def stop(self, train_idx):
        self.connector.move_train(self.current_track[0], 0, train_idx)

    def move(self, train_idx):
        if not self.should_stop(train_idx):
            if self.current_track[2] <= 0:
                # print(f'!!!!!!!!!!!!!!!   {self.current_track_idx}')
                self.current_track = list(self.path[self.current_track_idx])
                if self.connector.move_train(self.current_track[0], self.current_track[1], train_idx) == 4:
                    return 4
                self.current_track_idx += 1
            elif self.resume:
                self.connector.move_train(self.current_track[0], self.current_track[1], train_idx)
                self.resume = False
            self.current_track[2] -= 1
            self.tick += 1
            if self.current_track[2] <= 0 and self.current_track_idx == len(self.path):

                return False
        return True
