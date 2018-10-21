import numpy as np
import sys
from test_cases import TEST_CASES
from world import calc_score, MOVES, roll_coordinates, get_neighbours, apply_to_map, find_disjoint_components, update_direction
from solver import HC_1NB_CELLS, find_variants_for_mc
import time

_map, robots = TEST_CASES[29]
print(_map)
_map = np.array([list(l) for l in _map.split('\n')])

variants = find_variants_for_mc(_map)
hot_points = {}
for v in variants:
    hot_points[v[0]] = v[1]
arrows = {}

def move_till_hp_or_death(w, x, y, d, _map, visited_states, arrows, hot_points):
    sp = (x, y)
    arrows[sp] = w
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
    del arrows[sp]
    return w, x, y, d, is_live, new_visited_states

x, y, d = robots[0]
visited_states = set()

while True:
    hot_point = hot_points[(x, y)]
    del hot_points[(x, y)]

    ways = []
    for w in hot_point:
        ways.append(move_till_hp_or_death(w, x, y, d, _map, visited_states, arrows, hot_points))
    w, x, y, d, is_live, new_visited_states = max(ways, key=lambda x: (not x[4], len(x[5])))
    visited_states = visited_states.union(new_visited_states)
    arrows[(x, y)] = w