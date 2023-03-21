import numpy as np
import matplotlib.pyplot as plt
import matplotlib.collections as col

def is_point_in_circle(p1, p2, p3, v):
    x1, y1 = p1[0], p1[1]
    x2, y2 = p2[0], p2[1]
    x3, y3 = p3[0], p3[1]
    x0, y0 = v[0], v[1]
    a = np.linalg.det([[x1, y1, 1], [x2, y2, 1], [x3, y3, 1]])
    b = np.linalg.det([[x1 ** 2 + y1 ** 2, y1, 1], [x2 ** 2 + y2 ** 2, y2, 1], [x3 ** 2 + y3 ** 2, y3, 1]])
    c = np.linalg.det([[x1 ** 2 + y1 ** 2, x1, 1], [x2 ** 2 + y2 ** 2, x2, 1], [x3 ** 2 + y3 ** 2, x3, 1]])
    d = np.linalg.det([[x1 ** 2 + y1 ** 2, x1, y1], [x2 ** 2 + y2 ** 2, x2, y2], [x3 ** 2 + y3 ** 2, x3, y3]])

    return (a * (x0 ** 2 + y0 ** 2) -  b * x0 + c * y0 - d) * np.sign(a) < 0

def print_lines(self):
    printed_lines = []
    for line in self.lines:
        printed_lines.append([(line.point1.x, line.point1.y), (line.point2.x, line.point2.y)])
    lc = col.LineCollection(printed_lines, linewidths=2)
    fig, ax = plt.subplots()
    ax.add_collection(lc)
    ax.autoscale()
    ax.margins(0.1)
    plt.show()

def main():
    triangles = [[[0, 1], [1, 2], [3, 4]]]
    points = [[0, 1], [1, 5], [1, 6]]
    for p in points:
        for i in range(len(triangles)):
            triangle = triangles[i]
            if is_point_in_circle(triangle[0], triangle[1], triangle[2], p):
                triangles.pop(i)
                triangles.append([triangle[0], triangle[1], p])
                triangles.append([triangle[1], triangle[2], p])
            i = i - 1

    lines = []
    for t in triangles:
        lines.append([(t[0][0], t[0][1]), (t[1][0], t[1][1])])
        lines.append([(t[1][0], t[1][1]), (t[2][0], t[2][1])])
        lines.append([(t[0][0], t[0][1]), (t[2][0], t[2][1])])

    lc = col.LineCollection(lines, linewidths=2)
    fig, ax = plt.subplots()
    ax.add_collection(lc)
    ax.autoscale()
    ax.margins(0.1)
    plt.show()

main()