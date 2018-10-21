import numpy as np
from world import get_neighbours, calc_score, find_disjoint_components, DIRECTIONS, MOVES, roll_coordinates, update_direction
import time

LIMIT = 0.9
ARROW_IS_HOT = True

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


def any_arrow(nb):
    for n in nb:
        if n[3] in DIRECTIONS:
            return True
    return False


def find_variants_for_mc(_map):
    variants = []
    for y, x in np.argwhere(_map == '.'):
        nb = get_neighbours(_map, x, y)
        hot = nb[0][4] != nb[1][4] or nb[2][4] != nb[3][4]
        if not hot and ARROW_IS_HOT:
            hot = any_arrow(nb)
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


def move_till_hp_or_death(w, x, y, d, _map, visited_states, arrows, hot_points):
    sp = (x, y)
    arrows[sp] = w
    x, y, d, is_live, new_visited_states = move_till_hp_or_death2(x, y, d, _map,  visited_states, arrows, hot_points)
    del arrows[sp]
    return w, x, y, d, is_live, new_visited_states


def move_till_hp_or_death2(x, y, d, _map, visited_states, arrows, hot_points):
    new_visited_states = set()
    d = update_direction(_map, x, y, d, arrows)
    is_live = True
    while is_live and (x, y) not in hot_points:
        new_visited_states.add((x, y, d))
        x += MOVES[d][0]
        y += MOVES[d][1]
        x, y = roll_coordinates(x, y)
        d = update_direction(_map, x, y, d, arrows)
        is_live = _map[y, x] != '#' and (x, y, d) not in visited_states and (x, y, d) not in new_visited_states
    return x, y, d, is_live, new_visited_states


def DO_SPLITTED_MONTE_CARLO(_map, robots, start_time, cutoff_score=0):
    components = find_disjoint_components(_map, robots)
    p2c = {}
    for i, cmp in enumerate(components):
        for p in cmp[1]:
            p2c[p] = i
    variants = find_variants_for_mc(_map)
    variants_splitted = [[] for i in range(len(components))]
    for v in variants:
        if v[0] in p2c:
            variants_splitted[p2c[v[0]]].append(v)
    scores = [calc_score(_map, c[0]) for c in components]
    results = [[]] * len(components)
    ds = [dict((v[0], '') for v in variants) for variants in variants_splitted]
    while True:
        elapsed_time = time.time() - start_time
        if elapsed_time > LIMIT:
            break
        for i in range(len(components)):
            variants = variants_splitted[i]
            d = ds[i]
            for v in variants:
                d[v[0]] = v[1][np.random.randint(0, len(v[1]))]
            sc = calc_score(_map, components[i][0], d)
            if sc > scores[i]:
                result = []
                for k in d:
                    if d[k] != '':
                        result.append((k[0], k[1], d[k]))
                scores[i] = sc
                results[i] = result
    if sum(scores) < cutoff_score:
        return []
    result = [item for sublist in results for item in sublist]
    return result


def DO_GREED(_map, robots):
    variants = find_variants_for_mc(_map)
    hot_points = {}
    for v in variants:
        hot_points[v[0]] = v[1]
    arrows = {}

    is_live = []
    states = []
    visited = []
    for x, y, d in robots:
        states.append((x, y, d))
        visited.append(set())
        is_live.append(True)

    while any(is_live):
        for i in range(len(robots)):
            x, y, d = states[i]
            sp = (x, y)
            if sp in hot_points:
                hot_point = hot_points[sp]
                del hot_points[sp]
                ways = []
                for w in hot_point:
                    if w == '':
                        continue
                    ways.append(move_till_hp_or_death(w, x, y, d, _map, visited[i], arrows, hot_points))
                w, x, y, d, is_live[i], new_visited_states = max(ways, key=lambda x: (x[4], len(x[5])))
                arrows[sp] = w
            else:
                x, y, d, is_live[i], new_visited_states = move_till_hp_or_death2(x, y, d, _map, visited[i], arrows, hot_points)
            visited[i] = visited[i].union(new_visited_states)
            states[i] = (x, y, d)

    result = []
    for e in arrows:
        result.append((e[0], e[1], arrows[e]))
    return result