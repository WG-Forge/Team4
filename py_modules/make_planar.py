""" Module for creating planar graph """
from py_modules.graph import Graph
from py_modules.point import Point

from py_modules.line import Line


screen_width = 1600
screen_height = 900


# def create_graph_from_layer(raw_graph, layer_info):
#     points = {}
#     lines = {}
#     for point in raw_graph['points']:
#         points[point['idx']] = Point(point['idx'], point['post_idx'])
#     for line in raw_graph['lines']:
#         point_list = [points[point] for point in line['points']]
#         lines[line['idx']] = Line(point_list, line['idx'], line['length'])
#     for point_dict in layer_info['coordinates']:
#         points[point_dict['idx']].set_coords(point_dict['x']*4, point_dict['y']*4)
#     graph = Graph(points, lines, raw_graph['name'], raw_graph['idx'])
#     return points, lines, graph


def create_graph_from_layer(raw_graph, layer_info, home):
    points = {}
    lines = {}
    for point in raw_graph['points']:
        if home == 57:
            fake_idx = point['idx']
        elif home == 66:
            fake_idx = vertical_reflection(point['idx'])
        elif home == 147:
            fake_idx = horizontal_reflection(point['idx'])
        elif home == 156:
            fake_idx = horizontal_reflection(vertical_reflection(point['idx']))
        else:
            raise Exception('Wrong home index.')
        points[fake_idx] = Point(point['idx'], point['post_idx'], fake_idx=fake_idx)

    for line in raw_graph['lines']:
        point_list = [points[point] for point in line['points']]
        lines[line['idx']] = Line(point_list, line['idx'], line['length'])
    for point_dict in layer_info['coordinates']:
        points[point_dict['idx']].set_coords(point_dict['x'] * 4, point_dict['y'] * 4)
    graph = Graph(points, lines, raw_graph['name'], raw_graph['idx'])
    return points, lines, graph


def vertical_reflection(idx):
    left_in_row = ((idx - 57) // 10) * 10 + 57
    right_in_row = left_in_row + 9
    return left_in_row + right_in_row - idx


def horizontal_reflection(idx):
    real_row = (idx - 57) // 10
    fake_row = 9 - real_row
    left_in_row = real_row * 10 + 57
    diff = idx - left_in_row
    fake_left_in_row = fake_row * 10 + 57
    return fake_left_in_row + diff