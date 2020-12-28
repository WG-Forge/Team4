import pygame

from py_modules.line import Line
from py_modules.constants import *


class Train:
    def __init__(self, train_dict: dict):
        self.idx = train_dict['idx']
        self.goods = (train_dict['goods'], train_dict['goods_capacity'])
        self.line_idx = train_dict['line_idx']
        self.position = train_dict['position']
        self.speed = train_dict['speed']
        self.line = None
        self.coordinates = [0, 0]
        self.font = pygame.font.SysFont('arial', 20)
        self.goods_type = train_dict['goods_type']
        self.upgrade_cost = train_dict['next_level_price']
        self.crash_timer = 0
        self.enemy = False
        self.loading = False

    def set_line(self, line: Line):
        self.line = line

    def draw(self, screen, surface):
        threshold = (self.idx-1) * 150
        info = {'current line': [str(self.line_idx)], 'position': [self.position, self.line.length],
                'type of goods': [str(self.goods_type)], 'goods': self.goods}
        i = 5
        for key, value in info.items():
            if len(value) == 1:
                text2 = self.font.render(value[0], True, WHITE)
            else:
                text2 = self.font.render('{0}/{1}'.format(value[0], value[1]), True, WHITE)
            text1 = self.font.render(key, True, WHITE)
            screen.blit(text1, (1300, threshold+i))
            screen.blit(text2, (1500, threshold+i))
            i += 30
        step_x = (self.line.points[1].coordinates[0] - self.line.points[0].coordinates[0]) / self.line.length
        step_y = (self.line.points[1].coordinates[1] - self.line.points[0].coordinates[1]) / self.line.length
        self.coordinates[0] = self.line.points[0].coordinates[0] + step_x * self.position
        self.coordinates[1] = self.line.points[0].coordinates[1] + step_y * self.position
        pygame.draw.rect(screen,
                         train_colors[self.idx],
                         (1250, threshold+5, 300, 120), 1)
        pygame.draw.rect(surface,
                         train_colors[self.idx],
                         (int(self.coordinates[0]) - 8, int(self.coordinates[1]) - 8,
                          16,
                          16), 1)

    def update(self, train_dict: dict):
        if train_dict['goods'] > self.goods[0]:
            self.loading = True
        else:
            self.loading = False
        self.goods = (train_dict['goods'], train_dict['goods_capacity'])
        self.line_idx = train_dict['line_idx']
        self.position = train_dict['position']
        self.speed = train_dict['speed']
        self.goods_type = train_dict['goods_type']
        self.upgrade_cost = train_dict['next_level_price']
        if train_dict['events']:
            self.crash_timer = train_dict['cooldown']
            print('crash')
