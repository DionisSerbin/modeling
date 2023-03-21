import random
import matplotlib.pyplot as plt


class Automata:
    def __init__(self, matrix, chain_size, current_state):
        self.matrix = matrix
        self.chain_size = chain_size
        self.current_state = current_state

    def gen_seq(self):
        while self.current_state != 2:
            val = random.random()
            self.chain_size += 1
            state = 0
            while state < len(self.matrix[self.current_state]) and val >= self.matrix[self.current_state][state]:
                state += 1
            self.current_state = state
        return self.chain_size


def avg(y_s):
    return sum(y_s) / len(y_s)


def gen_dist(eps, matrix):
    matr = []
    for i in range(len(matrix)):
        matr.append([])
        for j in range(len(matrix)):
            matr[i].append(sum(matrix[i][:(j + 1)]))
    y_s = []
    res = []
    avg_range = 3
    for i in range(10):
        aut = Automata(
            matrix=matr,
            chain_size=0,
            current_state=0
        )
        y_s.append(aut.gen_seq())
        res.append(avg(y_s))

    while (max(res[-avg_range:]) - min(res[-avg_range:])) > 2 * eps:
        aut = Automata(
            matrix=matr,
            chain_size=0,
            current_state=0
        )
        y_s.append(aut.gen_seq())
        res.append(avg(y_s))
    return res, sum(res[-3:]) / 3, len(res)


def gen_res(matr, eps=0.0001):
    res, avg, iter = gen_dist(eps, matr)
    xs = list(range(len(res)))
    plt.plot(xs, res)
    plt.show()
    print(avg, iter)


if __name__ == '__main__':
    eps = 0.0001

    m_shoot = [
        [0.2, 0.5, 0.3],
        [0, 0.6, 0.4],
        [0, 0, 1]
    ]

    m_hw = [
        [0.3, 0.4, 0.3],
        [0, 0.2, 0.8],
        [0, 0, 1]
    ]

    gen_res(matr=m_shoot)
    gen_res(matr=m_hw)
