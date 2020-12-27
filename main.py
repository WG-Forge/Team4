"""
This this the starting function of the project. Here the Game class is created and is being run.
"""
import threading
import time
import pygame
import sys

from py_modules.post import Post
from py_modules.train import Train
from py_modules.dispatcher import Dispatcher
from py_modules.make_planar import create_graph_from_layer
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
        self.disp = None
        self.posts = {}
        self.trains = {}
        self.connector = None
        self.player_idx = None

        adjust_win_resolution()
        pygame.display.init()
        self.sc = pygame.display.set_mode((screen_width, screen_height))
        pygame.font.init()
        self.image = pygame.Surface([900, 900])

    def update_function(self):
        # with open('output.txt', 'a') as f:
        running = True
        while self.graph.tick < 500 and running:

            start = time.time()
            info = self.connector.get_info()
            self.update_map(self.posts, info)
            self.graph.tick += 1
            self.disp.do_tasks()
            for key, train in self.trains.items():
                train.update(info['trains'][key - 1])
            self.graph.rating = info['ratings'][self.player_idx]['rating']
            if self.graph.tick % 4 == 1:
                if self.selected is not None:
                    self.selected.draw(self.image, self.sc)
                self.update_screen(self.graph)
            if time.time()-start > 0.9:
                print(time.time()-start)
            else:
                self.connector.next_turn()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    break

    def run(self):
        try:
            self.connector = Connector()
        except Exception as e:
            print("something's wrong with the server. Exception is %s" % e)
            return
        self.connector.login('team', game_name='Game of the Year')
        player_info, zero_layer_info, first_layer_info, ten_layer_info = self.connector.get_map()
        raw_graph = zero_layer_info
        self.player_idx = player_info['idx']
        points, lines, self.graph = create_graph_from_layer(raw_graph, ten_layer_info, player_info['home']['idx'])
        self.graph.home = points[player_info['home']['idx']]
        points[player_info['home']['idx']].home = True
        points[player_info['home']['idx']].selected = True
        for post in first_layer_info['posts']:
            points[post['point_idx']].post = Post(post)
            self.posts[post['idx']] = points[post['point_idx']]
        self.graph.posts = self.posts
        self.trains = {train['idx']: Train(train) for train in player_info['trains']}
        self.graph.trains = self.trains
        for train in self.trains.values():
            train.set_line(lines[train.line_idx])
        self.disp = Dispatcher(self.graph, self.connector)
        self.disp.prepare()
        self.update_function()
        print(self.graph.rating)
        self.connector.close_conn()
        # thread.start()
        # while self.running:
        #     self.clock.tick(60)
            # for event in pygame.event.get():
            #     if event.type == pygame.QUIT:
            #         self.connector.close_conn()
            #         self.running = False
            #     if event.type == pygame.MOUSEBUTTONDOWN:
            #         if event.button == 1:
            #             if self.selected is not None:
            #                 self.selected.draw(self.image, self.sc)
            #             self.selected = self.mouse_click(event.pos, points)
            #             self.sc.blit(self.image, (100, 0))
            #             pygame.display.update()
            #         elif event.button == 3:
            #             old_mouse_x, old_mouse_y = event.pos
            #             self.dragging = True
            #         elif event.button == 4:
            #             self.graph.zoom(0.1)
            #         elif event.button == 5:
            #             self.graph.zoom(-0.1)
            #         self.update_screen(self.graph)
            #     elif event.type == pygame.MOUSEBUTTONUP:
            #         if event.button == 3:
            #             self.dragging = False
            #     elif event.type == pygame.MOUSEMOTION:
            #         if self.dragging:
            #             mouse_x, mouse_y = event.pos
            #             self.graph.move(mouse_x - old_mouse_x, mouse_y - old_mouse_y)
            #             old_mouse_x, old_mouse_y = event.pos
            #         self.update_screen(self.graph)

    # def mouse_click(self, mouse_pos: tuple, points: dict):
    #     """
    #     Checks if any point was selected
    #     :param mouse_pos: position of the mouse
    #     :param points: a dict of points
    #     :return: Point that was selected
    #     """
    #     if self.selected is not None:
    #         self.selected.selected = False
    #     if 100 < mouse_pos[0] < 1000:
    #         for point in points.values():
    #             if point.coordinates[0] - 7 < mouse_pos[0] - 100 < point.coordinates[0] + 7:
    #                 if point.coordinates[1] - 7 < mouse_pos[1] < point.coordinates[1] + 7:
    #                     point.selected = True
    #                     return point
    #     return None

    def update_map(self, posts, info):
        # for event in info['posts'][0]['events']:
        #     print(event)
        #     print(self.graph.tick)
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
