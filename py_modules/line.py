import pygame
from py_modules.constants import *


class Line:
    def __init__(self, points, idx=None, length=None):
        self.idx = idx
        self.length = length
        self.points = points

    def get_points(self):
        return [point.fake_idx for point in self.points]

    def draw(self, screen):
        # font = pygame.font.SysFont('arial', 20)
        # text = font.render(str(self.idx), True, WHITE)
        #
        # coordinates = [0, 0]
        # coordinates[0] = (self.points[0].coordinates[0] + self.points[1].coordinates[0]) / 2
        # coordinates[1] = (self.points[0].coordinates[1] + self.points[1].coordinates[1]) / 2
        # screen.blit(text, (int(coordinates[0]), int(coordinates[1])))

        pygame.draw.aaline(screen, WHITE, (int(self.points[0].coordinates[0]), int(self.points[0].coordinates[1])),
                           (int(self.points[1].coordinates[0]), int(self.points[1].coordinates[1])))