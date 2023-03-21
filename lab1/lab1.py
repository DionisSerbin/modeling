import math
import matplotlib.pyplot as plt


class GalileoMethod:
    def __init__(self, alpha, v_0):
        self.alpha = alpha
        self.v_0 = v_0
        self.g = 9.81

    def solve(self):
        self.x = self.v_0 * self.v_0 * math.sin(math.radians(self.alpha * 2)) / self.g
        return self.x

    def get_max_y(self):
        self.y = self.v_0 ** 2 * math.sin(math.radians(self.alpha)) ** 2 / (2 * self.g)
        return self.y


class NewtonMethod:
    def __init__(self, p, s, m, v_0, alpha, t, h, g):
        self.c = 0.15
        self.p = p
        self.s = s
        self.m = m
        self.b = self.c * self.p * self.s / 2
        self.v_0 = v_0
        self.angle = math.radians(alpha)
        self.t = t
        self.h = h
        self.g = g

    def solve(self):
        speed = [(self.cals_v_x(self.v_0, self.angle), self.calc_v_y(self.v_0, self.angle, 0))]
        self.coord = [(0, 0)]

        while self.coord[-1][1] >= 0:
            cur_v_x = speed[-1][0]
            cur_v_y = speed[-1][1]

            k1_x = self.h * self.calc_der_v_x(self.b, self.m, cur_v_x, cur_v_y)
            k1_y = self.h * self.calc_der_v_y(self.b, self.m, cur_v_x, cur_v_y)

            k2_x = self.h * self.calc_der_v_x(self.b, self.m, cur_v_x + k1_x / 2, cur_v_y + k1_y / 2)
            k2_y = self.h * self.calc_der_v_y(self.b, self.m, cur_v_x + k1_x / 2, cur_v_y + k1_y / 2)

            k3_x = self.h * self.calc_der_v_x(self.b, self.m, cur_v_x + k2_x / 2, cur_v_y + k2_y / 2)
            k3_y = self.h * self.calc_der_v_y(self.b, self.m, cur_v_x + k2_x / 2, cur_v_y + k2_y / 2)

            k4_x = self.h * self.calc_der_v_x(self.b, self.m, cur_v_x + k3_x / 2, cur_v_y + k3_y / 2)
            k4_y = self.h * self.calc_der_v_y(self.b, self.m, cur_v_x + k3_x / 2, cur_v_y + k3_y / 2)

            cur_v_x += (k1_x + 2 * k2_x + 2 * k3_x + k4_x) / 6
            cur_v_y += (k1_y + 2 * k2_y + 2 * k3_y + k4_y) / 6

            speed.append((cur_v_x, cur_v_y))
            cur_coord = self.coord[-1]
            cur_v_x = cur_coord[0] + self.h * cur_v_x
            cur_v_y = cur_coord[1] + self.h * cur_v_y
            self.coord.append((cur_v_x, cur_v_y))

        return self.coord[-1][0]

    def get_max_y(self):
        x_coord, y_coord = self.get_coord()
        return max(y_coord)

    def calc_runge_cutte(self):
        pass

    def cals_v_x(self, v, angle):
        return v * math.cos(angle)

    def calc_v_y(self, v, angle, t):
        return v * math.sin(angle) - self.g * t

    def calc_der_v_x(self, b, m, v_x, v_y):
        return -b * v_x * math.sqrt(v_x ** 2 + v_y ** 2) / m

    def calc_der_v_y(self, b, m, v_x, v_y):
        return -b * v_y * math.sqrt(v_x ** 2 + v_y ** 2) / m - self.g

    def get_coord(self):
        x_coord, y_coord = list(zip(*self.coord))
        return x_coord, y_coord


def plot_by_arrays(x_or_y_newton, x_or_y_galileo, my_range, my_label_x, my_label_y, my_title):
    plt.plot(my_range, x_or_y_newton, 'blue')
    if x_or_y_galileo is not None:
        plt.plot(my_range, x_or_y_galileo, 'red')
    plt.xlabel(my_label_x)
    plt.ylabel(my_label_y)
    plt.title(my_title)
    plt.show()


def plotting_model(d, density, alpha_start, v_0_start, v_range, alpha_range):
    r = d / 2
    volume = (4 / 3) * math.pi * (r ** 3)
    m = volume * density

    nm = NewtonMethod(
        p=1.29,
        s=math.pi * r ** 2,
        m=m,
        v_0=v_0_start,
        alpha=alpha_start,
        t=0,
        h=0.001,
        g=9.81
    )
    x_newton = nm.solve()

    gm = GalileoMethod(
        alpha=alpha_start,
        v_0=v_0_start
    )
    x_galileo = gm.solve()

    print(f"Newton: {x_newton}")
    print(f"Galileo: {x_galileo}")
    print(abs(x_newton - x_galileo))

    x_coord, y_coord = nm.get_coord()
    print(f"Newton max y: {nm.get_max_y()}")
    print(f"Galileo max y: {gm.get_max_y()}")

    plt.plot(x_coord, y_coord)
    plt.show()


    x_coords_newton = []
    x_coords_galileo = []
    y_coords_newton = []
    y_coords_galileo = []

    for v_0 in v_range:
        nm = NewtonMethod(
            p=1.29,
            s=math.pi * r ** 2,
            m=m,
            v_0=v_0,
            alpha=alpha_start,
            t=0,
            h=0.001,
            g=9.81
        )

        x_newton = nm.solve()
        x_coords_newton.append(x_newton)
        y_coords_newton.append(nm.get_max_y())

        gm = GalileoMethod(
            alpha=alpha_start,
            v_0=v_0
        )

        x_galileo = gm.solve()
        x_coords_galileo.append(x_galileo)
        y_coords_galileo.append(gm.get_max_y())

    plot_by_arrays(
        x_or_y_newton=x_coords_newton,
        x_or_y_galileo=x_coords_galileo,
        my_range=v_range,
        my_label_x="Скорость",
        my_label_y="Расстояние",
        my_title="Зависимость расстояния от начальной скорости"
    )

    plot_by_arrays(
        x_or_y_newton=y_coords_newton,
        x_or_y_galileo=y_coords_galileo,
        my_range=v_range,
        my_label_x="Скорость",
        my_label_y="Высота",
        my_title="Зависимость высоты от начальной скорости"
    )

    x_coords_newton = []
    x_coords_galileo = []
    y_coords_newton = []
    y_coords_galileo = []

    for alpha in alpha_range:
        nm = NewtonMethod(
            p=1.29,
            s=math.pi * r ** 2,
            m=m,
            v_0=v_0_start,
            alpha=alpha,
            t=0,
            h=0.001,
            g=9.81
        )

        x_newton = nm.solve()
        x_coords_newton.append(x_newton)
        y_coords_newton.append(nm.get_max_y())

        gm = GalileoMethod(
            alpha=alpha,
            v_0=v_0_start
        )

        x_galileo = gm.solve()
        x_coords_galileo.append(x_galileo)
        y_coords_galileo.append(gm.get_max_y())

    plot_by_arrays(
        x_or_y_newton=x_coords_newton,
        x_or_y_galileo=x_coords_galileo,
        my_range=alpha_range,
        my_label_x="Угол",
        my_label_y="Расстояние",
        my_title="Зависимость расстояния от угла"
    )

    plot_by_arrays(
        x_or_y_newton=y_coords_newton,
        x_or_y_galileo=y_coords_galileo,
        my_range=alpha_range,
        my_label_x="Угол",
        my_label_y="Высота",
        my_title="Зависимость высоты от угла"
    )


if __name__ == '__main__':
    plotting_model(
        d=0.36,
        density=11340,
        alpha_start=59,
        v_0_start=140,
        v_range=[i for i in range(0, 100)],
        alpha_range=[i for i in range(0, 90)]
    )
