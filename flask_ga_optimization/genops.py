import numpy as np


def sbx_real(parent1, parent2, eta, low, up):
    if np.random.rand() <= 0.5:
        if abs(parent1 - parent2) > 1e-14:
            if parent1 < parent2:
                y1 = parent1
                y2 = parent2
            else:
                y1 = parent2
                y2 = parent1
            yl = low
            yu = up
            rand = np.random.rand()
            beta = 1.0 + (2.0 * (y1 - yl) / (y2 - y1))
            alpha = 2.0 - beta ** -(eta + 1.0)

            if rand <= (1.0 / alpha):
                betaq = (rand * alpha) ** (1.0 / (eta + 1.0))
            else:
                betaq = (1.0 / (2.0 - rand * alpha)) ** (1.0 / (eta + 1.0))

            c1 = 0.5 * ((y1 + y2) - betaq * (y2 - y1))
            beta = 1.0 + (2.0 * (yu - y2) / (y2 - y1))
            alpha = 2.0 - beta ** -(eta + 1.0)

            if rand <= (1.0 / alpha):
                betaq = (rand * alpha) ** (1.0 / (eta + 1.0))
            else:
                betaq = (1.0 / (2.0 - rand * alpha)) ** (1.0 / (eta + 1.0))

            c2 = 0.5 * ((y1 + y2) + betaq * (y2 - y1))
            if c1 < yl:
                c1 = yl
            if c2 < yl:
                c2 = yl
            if c1 > yu:
                c1 = yu
            if c2 > yu:
                c2 = yu
            if np.random.rand() <= 0.5:
                child1 = c2
                child2 = c1
            else:
                child1 = c1
                child2 = c2
        else:
            child1 = parent1
            child2 = parent2
    else:
        child1 = parent1
        child2 = parent2
    return child1, child2


def mutate_real(data, prob, eta, low, up):
    if np.random.rand() <= prob:
        y = data
        yl = low
        yu = up
        delta1 = (y-yl)/(yu-yl)
        delta2 = (yu-y)/(yu-yl)
        rnd = np.random.rand()
        mut_pow = 1.0/(eta+1.0)
        if rnd <= 0.5:
            xy = 1.0-delta1
            val = 2.0*rnd+(1.0-2.0*rnd)*(xy**(eta+1.0))
            deltaq = val**mut_pow - 1.0
        else:
            xy = 1.0 - delta2;
            val = 2.0*(1.0-rnd)+2.0*(rnd-0.5)*(xy**(eta+1.0))
            deltaq = 1.0 - (val**mut_pow)
        y = y + deltaq*(yu-yl)
        if y < yl:
            y = yl
        if y > yu:
            y = yu
        return y
    return data