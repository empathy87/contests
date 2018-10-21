import numpy as np
import sys
from test_cases import TEST_CASES
from world import calc_score, MOVES, roll_coordinates, get_neighbours, apply_to_map, find_disjoint_components, update_direction
from solver import HC_1NB_CELLS, find_variants_for_mc, move_till_hp_or_death, move_till_hp_or_death2
import time

_map, robots = TEST_CASES[29]
_map = np.array([list(l) for l in _map.split('\n')])

variants = find_variants_for_mc(_map)
hot_points = {}
for v in variants:
    hot_points[v[0]] = v[1]
arrows = {}




x, y, d = robots[0]
lv = True
visited = set()

result = rec(x, y, d, lv, _map, visited, arrows, hot_points, 0)
z = 0