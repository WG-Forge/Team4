"""
Disclaimer:
This project has a lot of commented lines of the next steps. In the next prs they will be uncommented

This this the starting function of the project. Here the Game class is created and is being run.
"""

import pygame
import sys

from py_modules.graph import Post, Train, Dispatcher
from py_modules.make_planar import create_graph
from py_modules.connector import Connector

screen_width = 1600
screen_height = 900


def adjust_win_resolution():
    """
    Makes the size of the window on Windows correct
    :return: None
    """
    if sys.platform == 'win32':
        import ctypes
        ctypes.windll.user32.SetProcessDPIAware()


class Game:
    def __init__(self):
        self.selected = None
        self.dragging = False
        self.running = True
        self.clock = pygame.time.Clock()

        adjust_win_resolution()
        pygame.display.init()
        self.sc = pygame.display.set_mode((screen_width, screen_height))
        pygame.font.init()
        self.image = pygame.Surface([900, 900])

    def run(self):
        try:
            connector = Connector()
        except Exception as e:
            print("something's wrong with the server. Exception is %s" % (e))
            return
        player_info, zero_layer_info, first_layer_info = connector.get_map()
        raw_graph = zero_layer_info
        points, lines, subgraph = create_graph(raw_graph)

        subgraph.home = points[player_info['home']['idx']]
        points[player_info['home']['idx']].home = True
        posts = {}
        for post in first_layer_info['posts']:
            points[post['point_idx']].post = Post(post)
            posts[post['idx']] = points[post['point_idx']]
        subgraph.posts = posts

        trains = {train['idx']: Train(train) for train in player_info['trains']}
        subgraph.trains = trains
        for train in trains.values():
            train.set_line(lines[train.line_idx])
        disp = Dispatcher(subgraph, connector)
        disp.prepare()
        while self.running:
            self.clock.tick(120)
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                #     if event.key == pygame.K_u:
                #         connector.upgrade()
                    if event.key == pygame.K_SPACE:
                        disp.do_tasks()
                        info = connector.get_info()
                        self.update_map(posts, info)
                #         subgraph.rating = info['ratings'][player_idx]['rating']
                        if self.selected is not None:
                            self.selected.draw(self.image, self.sc)
                        for train in trains.values():
                            train.update(info['trains'][0])

                if event.type == pygame.QUIT:
                    connector.close_conn()
                    self.running = False
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if event.button == 1:
                        if self.selected is not None:
                            self.selected.draw(self.image, self.sc)
                        self.selected = self.mouse_click(event.pos, points)
                        self.sc.blit(self.image, (100, 0))
                        pygame.display.update()
                    elif event.button == 3:
                        old_mouse_x, old_mouse_y = event.pos
                        self.dragging = True
                    elif event.button == 4:
                        subgraph.zoom(0.1)
                    elif event.button == 5:
                        subgraph.zoom(-0.1)
                elif event.type == pygame.MOUSEBUTTONUP:
                    if event.button == 3:
                        self.dragging = False
                elif event.type == pygame.MOUSEMOTION:
                    if self.dragging:
                        mouse_x, mouse_y = event.pos
                        subgraph.move(mouse_x - old_mouse_x, mouse_y - old_mouse_y)
                        old_mouse_x, old_mouse_y = event.pos
                self.update_screen(subgraph)

    def mouse_click(self, mouse_pos: tuple, points: dict):
        """
        Checks if any point was selected
        :param mouse_pos: position of the mouse
        :param points: a dict of points
        :return: Point that was selected
        """
        if self.selected is not None:
            self.selected.selected = False
        if 100 < mouse_pos[0] < 1000:
            for point in points.values():
                if point.coordinates[0] - 7 < mouse_pos[0] - 100 < point.coordinates[0] + 7:
                    if point.coordinates[1] - 7 < mouse_pos[1] < point.coordinates[1] + 7:
                        point.selected = True
                        return point
        return None

    def update_map(self, posts, info):
        for post in info['posts']:
            posts[post['idx']].post.update(post)

    def update_screen(self, subgraph):
        """
        Updates the screen
        :param subgraph: the graph
        :return: None
        """
        self.image.fill((12, 12, 12))
        self.sc.fill((0, 0, 0))
        subgraph.draw(self.image, self.sc)
        self.sc.blit(self.image, (100, 0))
        pygame.display.update()


def main():
    game = Game()
    game.run()


if __name__ == '__main__':
    main()
    raise SystemExit()
