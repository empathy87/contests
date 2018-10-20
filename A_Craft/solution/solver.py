import numpy as np
from world import get_neighbours


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