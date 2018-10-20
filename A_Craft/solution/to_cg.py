import numpy as np
import time

_map = []
for i in range(10):
    line = input()
    _map.append(list(line))
_map = np.array(_map)

robot_count = int(input())
robots = []
for i in range(robot_count):
    x, y, direction = input().split()
    x, y = int(x), int(y)
    robots.append((x, y, direction))

###################################################################
MOVES = {'U': [0, -1],
         'D': [0, 1],
         'R': [1, 0],
         'L': [-1, 0]}
DIRECTIONS = set(['U', 'D', 'R', 'L'])


def update_direction(_map, x, y, d, arrows=None):
    if arrows and (x, y) in arrows and arrows[(x, y)] != '':
        return arrows[(x, y)]
    return (d, _map[y, x])[_map[y, x] in DIRECTIONS]


def roll_coordinates(x, y):
    x = (x, 18)[x < 0]
    y = (y, 9)[y < 0]
    x = (x, 0)[x > 18]
    y = (y, 0)[y > 9]
    return x, y


def calc_score(_map, robots, arrows=None):
    score = 0
    for robot in robots:
        visited_states = set()
        x, y, d = robot
        d = update_direction(_map, x, y, d, arrows)
        is_live = True
        robot_score = 0
        while is_live:
            robot_score += 1
            visited_states.add((x, y, d))
            x += MOVES[d][0]
            y += MOVES[d][1]
            x, y = roll_coordinates(x, y)
            d = update_direction(_map, x, y, d, arrows)
            is_live = _map[y, x] != '#' and (x, y, d) not in visited_states
        score += robot_score

    return score


def get_neighbours(_map, x, y):
    neighbours = []
    for d in MOVES:
        nx, ny = roll_coordinates(x + MOVES[d][0], y + MOVES[d][1])
        nv = _map[ny, nx]
        is_space = nv == '#'
        neighbours.append((d, nx, ny, nv, is_space))
    return neighbours


def apply_to_map(_map, solution):
    for x, y, a in solution:
        _map[y, x] = a

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


def find_disjoint_components(_map, robots):
    points = set((e[1], e[0]) for e in np.argwhere(_map != '#'))
    components = []
    while len(points):
        p = points.pop()
        cmp = set([p])
        lst = [p]
        while len(lst):
            n_lst = []
            for e in lst:
                for nb in get_neighbours(_map, e[0], e[1]):
                    nb_xy = (nb[1], nb[2])
                    if not nb[4] and not nb_xy in cmp:
                        cmp.add(nb_xy)
                        n_lst.append(nb_xy)
                lst = n_lst
        points -= cmp
        components.append(cmp)
    result = []
    for cmp in components:
        rb = [r for r in robots if (r[0], r[1]) in cmp]
        if len(rb) == 0:
            continue
        result.append((rb, cmp))
    return result


def DO_SPLITTED_MONTE_CARLO(_map, robots, start_time):
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
        if elapsed_time > 0.8:
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
    result = [item for sublist in results for item in sublist]
    return result


start_time = time.time()
solution_part1 = HC_1NB_CELLS(_map)
apply_to_map(_map, solution_part1)

solution_part2 = DO_SPLITTED_MONTE_CARLO(_map, robots, start_time)

solution = solution_part1 + solution_part2

print(' '.join([f'{s[0]} {s[1]} {s[2]}' for s in solution]))