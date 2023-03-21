import math
import numpy as np
import pylab as pl
from matplotlib import collections as mc
import random


class Segment:
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

    def get_list(self):
        return [self.p1, self.p2]


class Triangle:
    def __init__(self, a, b, c):
        self.vertices = [a, b, c]

    def get_segments(self):
        a = self.vertices[0]
        b = self.vertices[1]
        c = self.vertices[2]
        return Segment(a, b), Segment(b, c), Segment(c, a)

    def get_two_closest(self, point):
        dist_a = Utils().dist(point, self.vertices[0])
        dist_b = Utils().dist(point, self.vertices[1])
        dist_c = Utils().dist(point, self.vertices[2])
        if dist_a < dist_b and dist_a < dist_c:
            return self.vertices[1], self.vertices[2]
        if dist_b < dist_c and dist_b < dist_a:
            return self.vertices[2], self.vertices[0]
        if dist_c < dist_b and dist_c < dist_a:
            return self.vertices[0], self.vertices[1]

    def __str__(self):
        return str(self.vertices)


class Utils:
    def __init__(self):
        pass

    def show_triangles(self, triangles):
        printed_lines = []
        for t in triangles:
            seg1, seg2, seg3 = t.get_segments()
            printed_lines += [seg1.get_list(), seg2.get_list(), seg3.get_list()]
        lc = mc.LineCollection(printed_lines, linewidths=2)
        fig, ax = pl.subplots(clear=True)
        ax.add_collection(lc)
        ax.autoscale()
        ax.margins(0.1)
        pl.show()
        fig.clear()

    def dist(self, a, b):
        return math.hypot(a[0] - b[0], a[1] - b[1])

    def get_point_and_radius(self, T):
        (x1, y1), (x2, y2), (x3, y3) = T
        A = np.array([[x3 - x1, y3 - y1], [x3 - x2, y3 - y2]])
        Y = np.array([(x3 ** 2 + y3 ** 2 - x1 ** 2 - y1 ** 2),
                      (x3 ** 2 + y3 ** 2 - x2 ** 2 - y2 ** 2)])
        if np.linalg.det(A) == 0:
            return False
        Ainv = np.linalg.inv(A)
        X = 0.5 * np.dot(Ainv, Y)
        x, y = X[0], X[1]
        r = math.sqrt((x - x1) ** 2 + (y - y1) ** 2)
        return (x, y), r

    def point_in_circle(self, triangle, point):
        c, r = self.get_point_and_radius(triangle.vertices)
        return self.dist(c, point) < r

    def l2(self, p1, p2):
        return np.sqrt(sum((a - b) ^ 2 for a, b in zip(p1, p2)))

    def check_circle_inner(self, cx, cy, r, px, py):
        return self.l2([cx, cy], [px, py]) <= r

    def geenerate_triangles_in_square(self, points, point_center):
        triangles = []
        triangles.append(Triangle(points[0], points[1], point_center))
        triangles.append(Triangle(points[1], points[2], point_center))
        triangles.append(Triangle(points[2], points[3], point_center))
        triangles.append(Triangle(points[3], points[0], point_center))
        return triangles


def delete_and_build(triangles, point):
    deleted_tr = []
    deleted_points = set()
    for i in range(len(triangles)):
        if Utils().point_in_circle(triangles[i], point):
            deleted_tr.append(triangles[i])
    for triangle in deleted_tr:
        triangles.remove(triangle)
        deleted_points.add(triangle.vertices[0])
        deleted_points.add(triangle.vertices[1])
        deleted_points.add(triangle.vertices[2])
    deleted_points = list(deleted_points)
    while len(deleted_points) > 1:
        contour_p = deleted_points[0]
        second_p = max(deleted_points[1:], key=lambda x: Utils().dist(x, contour_p))
        deleted_points.remove(second_p)
        if len(deleted_points) > 1:
            third_p = max(deleted_points[1:], key=lambda x: Utils().dist(x, contour_p))
            triangles.append(Triangle(contour_p, point, third_p))
        deleted_points.append(second_p)
        deleted_points.remove(contour_p)
        triangles.append(Triangle(contour_p, point, second_p))
    return triangles


def generate_points(n):
    points = []
    for i in range(0, n):
        points.append((random.randint(0, 10), random.randint(0, 10)))
    return points


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
    return (min_x, max_y), (max_x, max_y), (max_x, min_y), (min_x, min_y)


# pointss = generate_points(3)
# test_tr = Triangle((1, 2), (2, 4), (5, 1))
# Utils().point_in_circle(test_tr, (3, 2))
# Utils().show_triangles([test_tr])
#
# test_triangles = [test_tr]
# test_triangles = delete_and_build(test_triangles, (3, 2))
# print("sss")
# for t in test_triangles:
#     print(t)
# Utils().show_triangles(test_triangles)
#
# test_triangles = [test_tr]
# test_triangles = delete_and_build(test_triangles, (3, 2))
# test_triangles = delete_and_build(test_triangles, (2, 3))
# for t in test_triangles:
#     print(t)
# Utils().show_triangles(test_triangles)


def test_with_square():
    points_square = [(0, 0), (0, 10), (10, 10), (10, 0)]
    point = (4, 5)
    test_triangles = Utils().geenerate_triangles_in_square(
        points=points_square,
        point_center=point
    )
    Utils().show_triangles(test_triangles)

    points = generate_points(4)
    for point in points:
        test_triangles = delete_and_build(test_triangles, point)
        print("triangles:")
        for t in test_triangles:
            print(t)
        Utils().show_triangles(test_triangles)


test_with_square()
