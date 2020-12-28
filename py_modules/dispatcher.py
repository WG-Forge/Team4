from py_modules.graph import Graph
from py_modules.path import Path
from py_modules.constants import worst_chance, food_chance

from graphModule import getOptimalPath


class Dispatcher:
    def __init__(self, graph: Graph, connector):
        self.graph = graph
        self.best_paths = {}
        self.train_tasks = {}
        self.arrival_dict = {}
        self.arrival_list = []
        self.kill_points = []
        self.stop_kill = []
        self.home = graph.home
        self.connector = connector
        self.upgrade_dict = {'posts': [], 'trains': []}
        self.trains_idxes = [train.idx for train in self.graph.trains.values()]

    def get_best_path(self, point_a, point_b, train_lines=None, excluded_points=None):
        """
        Finds best way between two points
        :param point_a: start point
        :param point_b: finish point
        :param train_lines: if not None than start point is a train
        :param excluded_points: points to be removed from the path
        :return: list representation of the path
        """
        lines_list = []
        for line in self.graph.lines.values():
            points = line.get_points()
            if excluded_points is None or (
                    points[0] not in excluded_points.keys() and points[1] not in excluded_points.keys()):
                lines_list.append([line.idx, line.length, line.get_points()])
        if train_lines is not None:
            lines_list += train_lines
        return getOptimalPath(self.graph.points[point_a].idx, self.graph.points[point_b].idx, lines_list)

    def get_path_to_point(self, point_idx, train_idx):
        """
        Finds optimal path from current train position to a point
        :param point_idx: destination point
        :param train_idx: train
        :return: a path
        """
        lines = [[-1, self.graph.trains[train_idx].position,
                  [self.graph.trains[train_idx].line.points[0].idx, 0]],
                 [-2, self.graph.trains[train_idx].line.length - self.graph.trains[train_idx].position,
                  [0, self.graph.trains[train_idx].line.points[1].idx]]]
        best_path = self.get_best_path(0, point_idx, lines)
        best_path[0][0] = self.graph.trains[train_idx].line.idx
        return best_path

    def do_tasks(self):
        """
        Does tasks for all trains and assigns new if all tasks are done
        :return: None
        """
        for train, paths in self.train_tasks.items():
            if self.stop_kill[0]['turn'] == self.graph.tick and self.stop_kill[0]['train_idx'] == train:
                if self.home.post.dead_people < self.stop_kill[0]['remain_population']:
                    paths[0].stop(train)

                    self.stop_kill[0]['turn'] += 1
                    dict_to_add = {}
                    list_to_delete = []
                    last_add = None
                    rem_turns = self.home.post.product[0] // self.home.post.population[0]
                    if self.arrival_list[1][0] - self.arrival_list[0][0] < rem_turns:
                        self.arrival_dict[self.arrival_list[1][2]][self.arrival_list[1][0]].stop_dict[self.arrival_list[1][0]-2] = rem_turns - self.arrival_list[1][0] + self.arrival_list[0][0] + 1
                        print(f'{self.arrival_list[1][2]} will stop by {rem_turns - self.arrival_list[1][0] + self.arrival_list[0][0] + 1} turns')

                    # for key, value in self.arrival_dict[train].items():
                    #     if key > self.graph.tick:
                    #         dict_to_add[key+rem_turns] = value
                    #         list_to_delete.append(key)
                    #         for point in self.arrival_list:
                    #             if point[0]-key <= rem_turns:
                    #                 self.train_tasks[point[2]][0].stop_dict


                    # for key, value in self.arrival_dict[train].items():
                    #     if key > self.graph.tick:
                    #         dict_to_add[key + 1] = value
                    #         list_to_delete.append(key)
                    #         last_add
                    #         # self.arrival_dict[train][key+1] = value
                    #         # del self.arrival_dict[train][key]
                    #         for point in self.arrival_list:
                    #             if key+1 == point[0]:
                    #                 self.stop_kill.append({'turn': point[2]-2, 'people_to_kill': 0, 'train_idx': point[2]})
                    # for point in list_to_delete:

                    print('stopped')
                    continue
                else:
                    paths[0].resume = True
            if not paths:
                continue
            if paths[0] == 'upgrade':
                self.upgrade_dict['trains'].append(train)
                if self.upgrade(train) != 4:
                    paths.pop(0)
            elif paths[0] == 'upgrade2':
                self.upgrade_dict['trains'].append(train)
                self.upgrade_dict['trains'].append(train)
                if self.upgrade(train) != 4:
                    paths.pop(0)
                else:
                    return False
            elif paths[0] == 'upgrade_town':
                self.upgrade_dict['posts'].append(self.home.post.post_idx)
                if self.upgrade(post=True) != 4:
                    paths.pop(0)
            if paths[0].move(train) is False:
                print('train {0} on turn {1}'.format(train, self.graph.tick))
                self.arrival_list.pop()
                paths.pop(0)
        return True

    def add_path(self, start, end, post_type, excluded_points=None):
        path = self.get_best_path(start, end, excluded_points=excluded_points)
        distance = 0
        posts = {}
        for line in path:
            line.append(self.graph.lines[line[0]].length)
            distance += line[2]
            point = self.graph.lines[line[0]].points[0] if line[1] == -1 else self.graph.lines[line[0]].points[1]
            if point.post is not None and post_type == point.post.type:
                posts[distance] = point.post
        self.best_paths[(start, end)] = Path(path, distance, self.connector)
        return start, end

    def combine_paths(self, *paths):
        path_list = []
        length = 0
        posts = {}
        if len(paths) == 1:
            paths = paths[0]
        for path in paths:
            path_list += path.path
            # if path.posts is not None:
            #     for turn, post in path.posts.items():
            #         posts[turn + length] = post
            length += path.length
        return Path(path_list, length, paths[0].connector)

    def create_path_through_points(self, *points, post_type=3):
        index = tuple(points)
        paths = []
        for i in range(len(points)-1):
            paths.append(self.add_path(points[i], points[i+1], post_type))
        self.best_paths[index] = self.combine_paths([self.best_paths[i] for i in paths])

    def make_prediction(self, turn, tick=None, food_source=False):
        if tick is None:
            tick = self.graph.tick
        remain_turns = 500-tick-turn
        current_food = 0 if food_source else self.home.post.product[0]
        self.kill_points = []
        death_idx = -1
        for arrival in self.arrival_list:
            if arrival[0] > tick:
                consume = 0
                consume += (arrival[0]-tick-1) * self.home.post.population[0]
                consume += (arrival[0] - tick) // 25 if tick > 125 else max(0, (arrival[0] - 125)//25)
                est_consume = consume + food_chance[max(arrival[0] - tick - turn - 1, 0)]
                worst_consume = consume + worst_chance[max(arrival[0] - tick - turn - 1, 0)]
                self.kill_points.append([arrival[0]-1, est_consume-current_food, worst_consume-current_food])
                if est_consume > current_food:
                    print('death {0} by {1}'.format(arrival[0]-1, est_consume-current_food))
                    break
                else:
                    if worst_consume > current_food:
                        death_idx = arrival[0] - 1
                        print('probable death {0} by {1}'.format(arrival[0] - 1, worst_consume - current_food))
                        break
                    current_food += arrival[1]
        print(self.kill_points)
        if death_idx > 0 and len(self.stop_kill) == 0:
            for point in self.kill_points:
                if point[2] > -5:
                    self.stop_kill.append({'turn': point[0], 'remain_population': 2, 'train_idx': arrival[2]})
                    break

        print(self.stop_kill)

    def prepare(self):
        self.create_path_through_points(57, 61, 101, 97, 57)
        self.create_path_through_points(57, 67, 90, 87, 57)
        self.create_path_through_points(57, 60, 90, 87, 57)
        self.create_path_through_points(57, 61, 101, 102, 97, 57)

        self.best_paths['armor'] = self.best_paths[(57, 61, 101, 97, 57)]
        self.best_paths['product1'] = self.best_paths[(57, 67, 90, 87, 57)]
        self.best_paths['product2'] = self.best_paths[(57, 60, 90, 87, 57)]
        self.best_paths['armor1'] = self.best_paths[(57, 61, 101, 102, 97, 57)]

        self.tactics_assign()

    def tactics_assign(self):

        paths = {1: self.best_paths['armor'].copy(),
                 2: self.best_paths['armor'].copy(),
                 3: self.best_paths['product1'].copy(),
                 4: self.best_paths['armor'].copy()}
        paths[1].stop_dict = {0: 2, 34: 4, 35: 7, 36: 31}
        paths[2].stop_dict[36] = 4
        paths[4].stop_dict = {0: 1, 35: 4, 36: 7}
        paths[5] = self.best_paths['armor'].copy()
        paths[5].stop_dict = {36: 28}
        paths[6] = self.best_paths['armor1'].copy()
        paths[6].stop_dict = {0: 2, 34: 4, 35: 7, 40: 23}
        paths[8] = self.best_paths['armor'].copy()
        paths[8].stop_dict = {36: 11}

        self.train_tasks[self.trains_idxes[0]] = ['upgrade2', paths[1], self.best_paths['product2'].copy(),
                                                  self.best_paths['product2'].copy(),
                                                  self.best_paths['product2'].copy(),
                                                  self.best_paths['product2'].copy(),
                                                  self.best_paths['product2'].copy(),
                                                  self.best_paths['product2'].copy(),
                                                  self.best_paths['product2'].copy(),
                                                  self.best_paths['product2'].copy()]
        self.train_tasks[self.trains_idxes[1]] = [paths[2], 'upgrade', self.best_paths['product2'].copy(), 'upgrade',
                                                  paths[5], 'upgrade_town', self.best_paths['product2'].copy(),
                                                  self.best_paths['product2'].copy(),
                                                  self.best_paths['product2'].copy(),
                                                  self.best_paths['product2'].copy(),
                                                  self.best_paths['product2'].copy(),
                                                  self.best_paths['product2'].copy(),
                                                  self.best_paths['product2'].copy()]
        self.train_tasks[self.trains_idxes[2]] = [paths[3], self.best_paths['product2'].copy(), 'upgrade',  paths[8],
                                                  'upgrade_town', self.best_paths['product2'].copy(),
                                                  self.best_paths['product2'].copy(),
                                                  self.best_paths['product2'].copy(),
                                                  self.best_paths['product2'].copy(),
                                                  self.best_paths['product2'].copy(),
                                                  self.best_paths['product2'].copy()]
        self.train_tasks[self.trains_idxes[3]] = [paths[4], 'upgrade', self.best_paths['product2'].copy(), 'upgrade',
                                                  self.best_paths['product2'].copy(),
                                                  self.best_paths['product2'].copy(),
                                                  self.best_paths['product2'].copy(),
                                                  self.best_paths['product2'].copy(),
                                                  self.best_paths['product2'].copy(),
                                                  self.best_paths['product2'].copy(),
                                                  self.best_paths['product2'].copy()]

        for train, task_list in self.train_tasks.items():
            capacity = 40
            timer = 0
            self.arrival_dict[train] = {}
            for task in task_list:
                if task == 'upgrade':
                    capacity *= 2
                elif task == 'upgrade2':
                    capacity *= 4
                elif type(task) is not str:
                    timer += sum([wait_timer for wait_timer in task.stop_dict.values()]) + task.length
                    if task.length < 60:
                        self.arrival_dict[train][timer] = capacity
                        self.arrival_list.append([timer, capacity, train])

        self.arrival_list.sort(key=lambda item: item[0])
        self.make_prediction(60)

    def upgrade(self, *train_idxes, post=False):
        response = self.upgrade_server()
        if response != 4:
            if post:
                self.graph.home.post.upgrade_cost *= 2
            for train_idx in train_idxes:
                self.graph.trains[train_idx].goods = (0, self.graph.trains[train_idx].goods[1] * 2)
                self.graph.home.post.armor = (self.graph.home.post.armor[0]-self.graph.trains[train_idx].upgrade_cost, self.graph.home.post.armor[1])
                self.graph.trains[train_idx].upgrade_cost *= 2
        return response

    def upgrade_server(self):
        response = self.connector.upgrade(self.upgrade_dict)
        for value in self.upgrade_dict.values():
            value.clear()
        return response
