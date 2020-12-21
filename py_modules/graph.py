""" This module contains the main classes """
import os
import sys
import random

import pygame

# from graphModule import getOptimalPath

screen_width = 1600
screen_height = 900
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
YELLOW = (225, 225, 0)
BLUE = (0, 0, 255)
DARK_BLUE = (0, 0, 100)
RED = (200, 0, 0)
DARK_RED = (100, 0, 0)
GREEN = (0, 200, 0)
DARK_GREEN = (0, 100, 0)
colors = [YELLOW, RED, GREEN, BLUE, WHITE]
type_colors = {"armor": [BLUE, DARK_BLUE], "population": [RED, DARK_RED], "product": [GREEN, DARK_GREEN]}


class Point:
    def __init__(self, idx: int, post_idx: int=None, coordinates: list=None):
        self.idx = idx
        self.post_idx = post_idx
        self.original_coordinates = coordinates
        self.coordinates = coordinates  # zoomed
        self.adjacent_points = []
        self.faces = []
        self.post = None
        self.home = False
        self.scale = 1
        self.selected = False

    def set_coords(self, x: int, y: int):
        self.original_coordinates = [x, y]
        self.coordinates = [x, y]

    def set_adjacent_points(self, points):
        self.adjacent_points = points

    def draw_table(self, info, screen):
        font = pygame.font.SysFont('arial', 20)
        i = 0
        for key, string in info.items():
            text1 = font.render(key, True, WHITE)
            if len(string) == 2:
                pygame.draw.rect(screen, type_colors[key][1], (screen_width - 200, screen_height - 20 - i, 100, 20))
                text2 = font.render('{0}/{1}'.format(string[0], string[1]), True, WHITE)
                pygame.draw.rect(screen, type_colors[key][0], (
                    screen_width - 200, screen_height - 20 - i, int(100 * string[0] / string[1]), 20))
            else:
                text2 = font.render(str(string[0]), True, WHITE)
            screen.blit(text1, (screen_width - 400, screen_height - 20 - i))
            screen.blit(text2, (screen_width - 200, screen_height - 20 - i))
            i += 30

    def draw(self, surface: pygame.Surface, screen):
        size = 5
        if self.home:
            size *= 2
        if self.post is not None:
            # image_rect = self.post.image.get_rect()
            # image_rect.center = (int(self.coordinates[0]), int(self.coordinates[1]))
            # surface.blit(self.post.image, image_rect)
            info = self.post.get_info()
            color_type = self.post.type
        else:
            info = {"idx": [self.idx]}
            color_type = 0
        if self.selected:
            self.draw_table(info, screen)
            color_type = 4
        pygame.draw.circle(surface, colors[color_type], (int(self.coordinates[0]), int(self.coordinates[1])), size)


class Line:
    def __init__(self, points, idx=None, length=None):
        self.idx = idx
        self.length = length
        self.points = points

    def get_points(self):
        return [point.idx for point in self.points]

    def draw(self, screen):
        # font = pygame.font.SysFont('arial', 10)
        # text = font.render(str(self.length), True, WHITE)
        #
        # coordinates = [0, 0]
        # coordinates[0] = (self.points[0].coordinates[0] + self.points[1].coordinates[0]) / 2
        # coordinates[1] = (self.points[0].coordinates[1] + self.points[1].coordinates[1]) / 2
        # screen.blit(text, (int(coordinates[0]), int(coordinates[1])))

        pygame.draw.aaline(screen, WHITE, (int(self.points[0].coordinates[0]), int(self.points[0].coordinates[1])),
                           (int(self.points[1].coordinates[0]), int(self.points[1].coordinates[1])))


class Face:
    def __init__(self, points_dict: dict, points_list: list):
        self.points_dict = points_dict
        self.points_list = points_list

    def get_points(self):
        return [point.idx for point in self.points_dict.values()]

    def get_edges(self, a, b):
        indexes = sorted([self.points_list.index(a), self.points_list.index(b)])
        first_edge = self.points_list[indexes[1]:] + self.points_list[:indexes[0]]
        second_edge = self.points_list[indexes[0]:indexes[1]]
        return [first_edge, second_edge]


class Graph:
    def __init__(self, points: dict = None, lines=None, name=None, idx=None):
        self.points = {}
        self.lines = {}
        self.name = name
        self.idx = idx
        self.faces = []
        self.trains = {}
        self.posts = {}
        self.home = None
        if points is not None:
            self.points = points
        if lines is not None:
            self.lines = lines
        self.rating = 0
        self.scale = 1

    def get_biggest_face(self):
        faces_count = {self.faces.index(face): len(face.points_list) for face in self.faces}
        return self.faces[max(faces_count, key=faces_count.get)]

    def get_lines_by_path(self, path: list):
        pairs = [[path[i], path[i + 1]] for i in range(len(path) - 1)]
        return self.get_line_by_points(pairs)

    def get_line_by_points(self, pair_points):
        pair_points = [sorted(pair) for pair in pair_points]
        lines = {}
        for key, line in self.lines.items():
            if sorted(line.get_points()) in pair_points:
                lines[key] = line
        return lines

    def get_faces(self):
        return [face.get_points() for face in self.faces]

    def get_lines(self):
        return [line.get_points() for line in self.lines.values()]

    def draw(self, surface, screen):
        for line in self.lines.values():
            line.draw(surface)
        for point in self.points.values():
            point.draw(surface, screen)
        # self.display_rating(screen)
        # for train in self.trains.values():
        #     train.set_line(self.lines[train.line_idx])
        #     train.draw(screen, surface)

    def change_face(self, alpha_path: list, face_index: int):
        edges = self.faces[face_index].get_edges(alpha_path[0], alpha_path[-1])
        if edges[1][0] == alpha_path[0]:
            edges[0], edges[1] = edges[1], edges[0]
        old_list = [point for point in alpha_path[::-1] + edges[0][1:]]
        new_list = [point for point in alpha_path + edges[1][1:]]
        old_dict = {point: self.points[point] for point in old_list}
        new_dict = {point: self.points[point] for point in new_list}
        self.faces[face_index].points_dict = old_dict
        self.faces[face_index].points_list = old_list
        self.faces.append(Face(new_dict, new_list))

    def move(self, x, y):
        for point in self.points.values():
            point.coordinates[0] += x
            point.coordinates[1] += y

    def zoom(self, scale_increase):
        if 1 <= self.scale+scale_increase <= 3:
            self.scale += scale_increase
        for point in self.points.values():
            point.coordinates[0] = point.coordinates[0] / point.scale * self.scale
            point.coordinates[1] = point.coordinates[1] / point.scale * self.scale
            point.scale = self.scale

    # def display_rating(self, screen):
    #     font = pygame.font.SysFont('arial', 20)
    #     text1 = font.render(str(self.rating), True, WHITE)
    #     screen.blit(text1, (screen_width - 200, 320))
    #
    # def find_optimal_path(self, point1_idx: int, point2_idx: int):
    #     return getOptimalPath(point1_idx, point2_idx,
    #                           [[line.idx, line.length, line.get_points()] for line in self.lines.values()])


class Post:
    def __init__(self, post_dict: dict):
        self.name = post_dict['name']
        self.idx = post_dict['point_idx']
        self.post_idx = post_dict['idx']
        self.type = post_dict['type']
        if self.type == 1:
            # self.image_path = "pictures/city.png"
            self.armor = (post_dict['armor'], post_dict['armor_capacity'])
            self.population = (post_dict['population'], post_dict['population_capacity'])
            self.product = (post_dict['product'], post_dict['product_capacity'])
        elif self.type == 2:
            # self.image_path = "pictures/shop.png"
            self.product = (post_dict['product'], post_dict['product_capacity'])
            self.replenishment = post_dict['replenishment']
        elif self.type == 3:
            # self.image_path = "pictures/armour.png"
            self.armor = (post_dict['armor'], post_dict['armor_capacity'])
            self.replenishment = post_dict['replenishment']

        # image = pygame.image.load(self.resource_path()).convert_alpha()
        # self.image = pygame.transform.scale(image, (20, 20))

    # def resource_path(self):
    #     """ Get absolute path to resource, works for dev and for PyInstaller """
    #     try:
    #         # PyInstaller creates a temp folder and stores path in _MEIPASS
    #         base_path = sys._MEIPASS
    #     except Exception:
    #         base_path = os.path.abspath(".")
    #
    #     return os.path.join(base_path, self.image_path)

    def get_info(self) -> dict:
        info = {'name': [self.name], 'idx': [self.idx]}
        if self.type == 1:
            info['armor'] = [self.armor[0], self.armor[1]]
            info['population'] = [self.population[0], self.population[1]]
            info['product'] = [self.product[0], self.product[1]]
        elif self.type == 2:
            info['replenishment'] = [self.replenishment]
            info['product'] = [self.product[0], self.product[1]]
        elif self.type == 3:
            info['replenishment'] = [self.replenishment]
            info['armor'] = [self.armor[0], self.armor[1]]
        return info

    def update(self, post_dict: dict):
        if self.type == 1:
            self.armor = (post_dict['armor'], post_dict['armor_capacity'])
            self.population = (post_dict['population'], post_dict['population_capacity'])
            self.product = (post_dict['product'], post_dict['product_capacity'])
        elif self.type == 2:
            self.product = (post_dict['product'], post_dict['product_capacity'])
        elif self.type == 3:
            self.armor = (post_dict['armor'], post_dict['armor_capacity'])


# class Train:
#     def __init__(self, train_dict: dict):
#         self.idx = train_dict['idx']
#         # self.fuel = (train_dict['fuel'], train_dict['fuel_capacity'])
#         self.goods = (train_dict['goods'], train_dict['goods_capacity'])
#         self.line_idx = train_dict['line_idx']
#         self.position = train_dict['position']
#         self.speed = train_dict['speed']
#         self.line = None
#         self.coordinates = [0, 0]
#
#     def set_line(self, line: Line):
#         self.line = line
#
#     def draw(self, screen, surface):
#         pygame.draw.rect(screen, BLACK, (1400, 0, 100, 100), 0)
#         font = pygame.font.SysFont('arial', 20)
#         text = font.render(
#             str(self.line_idx) + ' ' + str(self.line.points[0].idx) + ' ' + '{0}/{1}'.format(self.position,
#                                                                                              self.line.length) + ' ' + str(
#                 self.line.points[1].idx) + ' ' + str(self.speed), True, WHITE)
#
#         text2 = font.render(str(self.goods[0]) + ' ' + str(self.goods[1]), True, WHITE)
#         screen.blit(text, (1400, 0))
#         screen.blit(text2, (1400, 20))
#         step_x = (self.line.points[1].coordinates[0] - self.line.points[0].coordinates[0]) / self.line.length
#         step_y = (self.line.points[1].coordinates[1] - self.line.points[0].coordinates[1]) / self.line.length
#         # self.coordinates[0] = (self.line.points[0].coordinates[0] + self.line.points[1].coordinates[0]) / 2
#         # self.coordinates[1] = (self.line.points[0].coordinates[1] + self.line.points[1].coordinates[1]) / 2
#         self.coordinates[0] = self.line.points[0].coordinates[0] + step_x * self.position
#         self.coordinates[1] = self.line.points[0].coordinates[1] + step_y * self.position
#         pygame.draw.circle(surface, BLUE, (int(self.coordinates[0]), int(self.coordinates[1])), 5, 0)
#
#     def get_possible_lines(self):
#         return self.line_idx
#
#     def update(self, train_dict: dict):
#         self.goods = (train_dict['goods'], train_dict['goods_capacity'])
#         self.line_idx = train_dict['line_idx']
#         self.position = train_dict['position']
#         self.speed = train_dict['speed']
#
#
# class Dispatcher:
#     def __init__(self, graph: Graph):
#         self.graph = graph
#         self.posts = {1: {}, 2: {}, 3: {}}
#         self.rem_length = 0
#         self.train_path = None
#         self.train_tasks = {}
#         for idx, post in self.graph.posts.items():
#             self.posts[post.post.type][post.idx] = post
#
#     def get_best_path(self, point_a, point_b, train_lines=None):
#         lines_list = [[line.idx, line.length, line.get_points()] for line in self.graph.lines.values()]
#         if train_lines is not None:
#             lines_list += train_lines
#         return getOptimalPath(point_a, point_b, lines_list)
#
#     def get_path_to_point(self, point_idx, train_idx):
#         lines = [[-1, self.graph.trains[train_idx].position,
#                   [self.graph.trains[train_idx].line.points[0].idx, 0]],
#                  [-2, self.graph.trains[train_idx].line.length - self.graph.trains[train_idx].position,
#                   [0, self.graph.trains[train_idx].line.points[1].idx]]]
#         best_path = self.get_best_path(0, point_idx, lines)
#         best_path[0][0] = self.graph.trains[train_idx].line.idx
#         return best_path
#
#     def move_train_to_point(self, point_idx, train_idx, connector):
#         if self.train_path is None:
#             self.train_path = self.get_path_to_point(point_idx, train_idx)
#             next_line = self.train_path[0]
#             self.rem_length = self.graph.lines[next_line[0]].length - self.graph.trains[train_idx].position \
#                 if self.train_path[0][1] == 1 else self.graph.trains[train_idx].position
#             if self.rem_length != 0:
#                 connector.move_train(next_line[0], next_line[1], train_idx)
#
#             self.train_path.pop(0)
#
#         if self.rem_length == 0:
#             if self.train_path:
#                 next_line = self.train_path.pop(0)
#                 connector.move_train(next_line[0], next_line[1], train_idx)
#                 self.rem_length = self.graph.lines[next_line[0]].length
#
#             else:
#                 self.train_path = None
#                 return 1
#         self.rem_length -= 1
#
#     def do_tasks(self, connector):
#         for train in self.train_tasks.keys():
#             if not self.train_tasks[train]:
#                 pass
#             else:
#                 self.train_path = self.train_tasks[train][0]
#                 if self.move_train_to_point(self.train_tasks[train][0], train, connector) == 1:
#                     self.train_tasks[train].pop(0)
#
#     def get_min_path(self, post_type, start, train_idx):
#         paths = {}
#         distances = {}
#         for idx, post in self.posts[post_type].items():
#             paths[idx] = self.get_best_path(start, idx)
#             distances[idx] = 0
#             for line in paths[idx]:
#                 line.append(self.graph.lines[line[0]].length)
#                 distances[idx] += line[2]
#         min_post = min(distances, key=distances.get)
#         if train_idx not in self.train_tasks:
#             self.train_tasks[train_idx] = []
#         # first_length = self.graph.trains[train_idx].line.length - self.graph.trains[train_idx].position \
#         #     if paths[min_post][0][1] == 1 else self.graph.trains[train_idx].position
#         path = Path(paths[min_post], start, min_post, distances[min_post])
#         self.train_tasks[train_idx].append(paths[min_post])
#         self.train_tasks[train_idx].append(self.get_best_path(min_post, start))
#
#     def get_armor(self, start):
#         self.get_min_path(3, start, 1)
#
#     def get_products(self, start):
#         self.get_min_path(2, start, 1)
#
#     def assign_tasks(self):
#         self.get_armor(self.graph.home.idx)
#         print(self.train_tasks)
#
#
# class Path:
#     def __init__(self, path, start, end, length):
#         self.path = path
#         self.end = end
#         self.length = length
#
#     def create_path(self):
#         pass