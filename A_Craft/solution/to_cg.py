import sys
import math
import numpy as np

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


def update_direction(_map, x, y, d):
    return (d, _map[y, x])[_map[y, x] in DIRECTIONS]


def roll_coordinates(x, y):
    x = (x, 18)[x < 0]
    y = (y, 9)[y < 0]
    x = (x, 0)[x > 18]
    y = (y, 0)[y > 9]
    return x, y


def get_neighbours(_map, x, y):
    neighbours = []
    for d in MOVES:
        nx, ny = roll_coordinates(x + MOVES[d][0], y + MOVES[d][1])
        nv = _map[ny, nx]
        is_space = nv == '#'
        neighbours.append((d, nx, ny, nv, is_space))
    return neighbours


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


solution_part1 = HC_1NB_CELLS(_map)

print(' '.join([f'{s[0]} {s[1]} {s[2]}' for s in solution_part1]))