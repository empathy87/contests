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

start_time = time.time()
solution_part1 = HC_1NB_CELLS(_map)
apply_to_map(_map, solution_part1)

solution_part2 = DO_MONTE_CARLO(_map, robots, start_time)

solution = solution_part1 + solution_part2

print(' '.join([f'{s[0]} {s[1]} {s[2]}' for s in solution]))