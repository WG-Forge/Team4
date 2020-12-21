""" Module for creating planar graph """
from py_modules.graph import *
from math import cos, sin, pi
from graphModule import getFragments, getAllowedFaces, getAlphaPath, newPosition, getCycle


def create_graph(raw_graph):
    points = {}
    lines = {}
    for point in raw_graph['points']:
        points[point['idx']] = Point(point['idx'], point['post_idx'])
    for line in raw_graph['lines']:
        point_list = [points[point] for point in line['points']]
        point_list[0].adjacent_points.append(point_list[1])
        point_list[1].adjacent_points.append(point_list[0])
        lines[line['idx']] = Line(point_list, line['idx'], line['length'])

    graph = Graph(points, lines, raw_graph['name'], raw_graph['idx'])
    cycle = getCycle(graph.get_lines())
    subgraph = cycle_to_graph(graph, cycle)
    subgraph.faces.append(Face(subgraph.points, cycle))
    subgraph.faces.append(Face(subgraph.points, cycle))

    prettify(graph, subgraph, points)
    draw_planar(subgraph, points)
    return points, lines, subgraph


def get_face_coordinates(N):
    """
    Creates point coordinates for outer edge
    :param N: number of outer edge points
    :return: a list of coordinates
    """
    r = 400
    screen_width = 900
    screen_height = 900
    x = {}
    y = {}
    for n in range(N):
        x[n] = int(r * cos(2*pi*n/N) + screen_width//2)
        y[n] = int(r * sin(2*pi*n/N) + screen_height//2)

    return [x, y]


def cycle_to_graph(graph: Graph, cycle: list) -> Graph:
    """
    Creates a Graph from cycle and graph
    :param graph: existing graph
    :param cycle: a cicle in graph
    :return: new graph
    """
    subgraph = Graph()
    point_pairs = []
    for i in range(len(cycle)):
        point_pairs.append([cycle[i - 1], cycle[i]])
        subgraph.points[cycle[i - 1]] = graph.points[cycle[i - 1]]
    lines = graph.get_line_by_points(point_pairs)
    subgraph.lines = lines
    return subgraph


def prettify(graph: Graph, subgraph: Graph, points: dict):
    """
    Finds and adds all faces of the subgraph
    :param graph: origin graph
    :param subgraph: new graph
    :param points: dict of points
    :return: None
    """
    while True:
        fragments = getFragments(graph.get_lines(), subgraph.get_lines())
        if not fragments:
            break
        allowed_faces_indexes = []
        for fragment in fragments:
            faces = subgraph.get_faces()
            allowed_faces_indexes.append(getAllowedFaces(sorted(fragment[0]), faces))
            if len(allowed_faces_indexes[-1]) < 2:
                break
        alpha_path = getAlphaPath(fragment[0], fragment[1])
        alpha_points = {point_idx: points[point_idx] for point_idx in alpha_path}
        subgraph.points = {**alpha_points, **subgraph.points}
        subgraph.change_face(alpha_path, allowed_faces_indexes[-1][0])
        subgraph.lines = {**graph.get_lines_by_path(alpha_path), **subgraph.lines}


def draw_planar(subgraph: Graph, points: dict):
    """
    Assigns the coordinates of all points of the graph
    :param subgraph: the graph
    :param points: a dict of points
    :return: None
    """
    face = subgraph.get_biggest_face()
    coords = get_face_coordinates(len(face.points_list))
    i = 0
    inner_points = dict(points)
    for point in face.points_dict.values():
        point.set_coords(coords[0][i], coords[1][i])
        del inner_points[point.idx]
        i += 1
    for point in inner_points.values():
        point.set_coords(random.randrange(screen_width // 2 - 150, screen_width // 2 + 150),
                         random.randrange(screen_height // 2 - 150, screen_height // 2 + 150))
    n = len(points)
    const = (n/pi)**0.5
    delta = 0.5
    old_coords = {}
    cool = (pi/n)**0.5/(1 + pi / n * i ** 1.5)
    while 1:
        for point in inner_points.values():
            old_coords[point.idx] = point.coordinates
        for _ in range(10):
            new_coords = {}
            for point in inner_points.values():
                neighbours = [neighbour.coordinates for neighbour in point.adjacent_points]
                new_coords[point.idx] = newPosition(point.coordinates, neighbours, 4 * cool, const)
            for point in inner_points.values():
                point.set_coords(new_coords[point.idx][0], new_coords[point.idx][1])
        stop = True
        for point in inner_points.values():
            if abs(old_coords[point.idx][0] - point.coordinates[0]) > delta or abs(
                    old_coords[point.idx][1] - point.coordinates[1]) > delta:
                stop = False
        if stop:
            break
