import numpy as np
from world import get_neighbours, calc_score
import time


def HC_1NB_CELLS(_map):
    result = []
    for y, x in np.argwhere(_map == '.'):
        nb = get_neighbours(_map, x, y)
        nb_ground = [e for e in nb if e[4] == False]
        if len(nb_ground) == 0:
            result.append((x, y, 'U'))
        if len(nb_ground) == 1:
            result.append((x, y, nb_ground[0][0]))
    return result


def find_variants_for_mc(_map):
    variants = []
    for y, x in np.argwhere(_map == '.'):
        nb = get_neighbours(_map, x, y)
        hot = nb[0][4] != nb[1][4] or nb[2][4] != nb[3][4]
        has = nb[0][4] == nb[1][4] or nb[2][4] == nb[3][4]
        if not hot:
            continue
        k = ([], [''])[has] + [e[0] for e in nb if not e[4]]
        if len(k) > 0:
            variants.append(((x, y), k))
    return variants


def DO_MONTE_CARLO(_map, robots, start_time):
    score = calc_score(_map, robots)
    variants = find_variants_for_mc(_map)
    result = []
    if len(variants) == 0:
        return result
    d = dict((v[0], '') for v in variants)
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time > 0.8:
            break
        for v in variants:
            d[v[0]] = v[1][np.random.randint(0, len(v[1]))]
        sc = calc_score(_map, robots, d)
        if sc > score:
            result = []
            for k in d:
                if d[k] != '':
                    result.append((k[0], k[1], d[k]))
            score = sc
    return result