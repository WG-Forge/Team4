import pygame
from py_modules.constants import *


screen_width = 1600
screen_height = 900


class Point:
    def __init__(self, idx: int, post_idx: int = None, fake_idx: int = None, coordinates: list = None):
        self.idx = idx
        self.post_idx = post_idx

        self.fake_idx = fake_idx if fake_idx is not None else idx

        self.original_coordinates = coordinates
        self.coordinates = coordinates  # zoomed
        self.post = None
        self.home = False
        self.scale = 1
        self.selected = False

    def set_coords(self, x: int, y: int):
        self.original_coordinates = [x, y]
        self.coordinates = [x, y]

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