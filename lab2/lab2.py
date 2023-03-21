import random

import numpy as np
import pylab as pl
from matplotlib import collections as mc


class Point:
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Line:
    def __init__(self, p1, p2):
        self.point1 = p1
        self.point2 = p2


class Triangle:
    def __init__(self, p1, p2, p3):
        self.verticies = [p1, p2, p3]
        self.p1 = p1
        self.p2 = p2
        self.p3 = p3
        self.lines = [Line(p1, p2), Line(p2, p3), Line(p3, p1)]

    def print_lines(self):
        printed_lines = []
        for line in self.lines:
            printed_lines.append([(line.point1.x, line.point1.y), (line.point2.x, line.point2.y)])
        lc = mc.LineCollection(printed_lines, linewidths=2)
        fig, ax = pl.subplots()
        ax.add_collection(lc)
        ax.autoscale()
        ax.margins(0.1)
        pl.show()


    def get_points(self):
        return self.p1, self.p2, self.p3


def point_in_circumscribed(triangle, point):
    x_0 = point.x
    y_0 = point.y
    x_1 = triangle.vertices[0].x
    y_1 = triangle.vertices[0].y
    x_2 = triangle.vertices[1].x
    y_2 = triangle.vertices[1].y
    x_3 = triangle.vertices[2].x
    y_3 = triangle.vertices[2].y

    check_res = ((x_0 - x_1) * (y_0 - y_3) - (x_0 - x_3) * (y_0 - y_1)) * (
            (x_2 - x_3) * (x_2 - x_1) + (y_2 - y_3) * (y_2 - y_1)) + (
                        (x_0 - x_1) * (x_0 - x_3) + (y_0 - y_1) * (y_0 - y_3)) * (
                        (x_2 - x_3) * (y_2 - y_1) - (x_2 - x_1) * (y_2 - y_3))

    return check_res < 0


# points = [Point(0, 0), Point(3, 0), Point(3, 2)]
# triangle = Triangle(points[0], points[1], points[2])
# triangle.print_lines()


def generate_points(n):
    points = []
    for i in range(0, n):
        points.append(Point(random.randint(0, 10), random.randint(0, 10)))
    return points


def generate_triangles(points):
    triangles = []
    range = 3
    i = 0
    while i < len(points):
        triangles.append(Triangle(points[i], points[i + 1], points[i + 2]))
        i = i + range
    return triangles

def get_rectangle_points(points):
    x_points = []
    y_points = []
    for point in points:
        x_points.append(point.x)
        y_points.append(point.y)
    min_x = min(x_points)
    min_y = min(y_points)
    max_x = max(x_points)
    max_y = max(y_points)
    # [(min_x, max_y), (max_x, max_y)]
    # [(min_x, min_y), (max_x, min_y)]
    return Point(min_x, max_y), Point(max_x, max_y), \
           Point(min_x, min_y), Point(max_x, min_y)


def print_triangles(triangles, points):
    printed_lines = []
    for triangle in triangles:
        for line in triangle.lines:
            printed_lines.append([
                (line.point1.x, line.point1.y),
                (line.point2.x, line.point2.y)
            ])
    lc = mc.LineCollection(printed_lines, linewidths=2)
    fig, ax = pl.subplots()
    pxY, pXY, pxy, pXy = get_rectangle_points(points)
    rect_lines = []
    rect_lines.append([
        (pxY.x, pxY.y),
        (pXY.x, pXY.y)
    ])
    rect_lines.append([
        (pXY.x, pXY.y),
        (pXy.x, pXy.y)
    ])
    rect_lines.append([
        (pXy.x, pXy.y),
        (pxy.x, pxy.y)
    ])
    rect_lines.append([
        (pxy.x, pxy.y),
        (pxY.x, pxY.y)
    ])
    rl = mc.LineCollection(rect_lines, colors=(0, 1, 0, 1), linewidths=2)
    ax.add_collection(lc)
    ax.add_collection(rl)
    ax.autoscale()
    ax.margins(0.1)
    pl.show()


generated_points = generate_points(12)
print_triangles(generate_triangles(generated_points), generated_points)



