""" This module contains the main classes """

from py_modules.constants import *
import pygame

screen_width = 1600
screen_height = 900


class Graph:
    def __init__(self, points: dict = None, lines=None, name=None, idx=None):
        self.points = {}
        self.lines = {}
        self.name = name
        self.idx = idx
        self.trains = {}
        self.posts = {}
        self.home = None
        self.tick = 0
        if points is not None:
            self.points = points
        if lines is not None:
            self.lines = lines
        self.rating = 0
        self.scale = 1

    def get_lines(self):
        return [line.get_points() for line in self.lines.values()]

    def draw(self, surface, screen):
        for line in self.lines.values():
            line.draw(surface)
        for point in self.points.values():
            point.draw(surface, screen)
        self.display_rating(screen)
        for train in self.trains.values():
            train.set_line(self.lines[train.line_idx])
            train.draw(screen, surface)

    # def move(self, x, y):
    #     for point in self.points.values():
    #         point.coordinates[0] += x
    #         point.coordinates[1] += y
    #
    # def zoom(self, scale_increase):
    #     if 1 <= self.scale + scale_increase <= 3:
    #         self.scale += scale_increase
    #     for point in self.points.values():
    #         point.coordinates[0] = point.coordinates[0] / point.scale * self.scale
    #         point.coordinates[1] = point.coordinates[1] / point.scale * self.scale
    #         point.scale = self.scale

    def display_rating(self, screen):
        font = pygame.font.SysFont('arial', 20)
        text1 = font.render(str(self.tick) + '   ' + str(self.rating), True, WHITE)
        screen.blit(text1, (screen_width - 200, 700))
