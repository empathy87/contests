import numpy as np
from test_cases import TEST_CASES
from world import calc_score, apply_to_map
from solver import HC_1NB_CELLS, DO_MONTE_CARLO
import time

test_case = 0
total_score = 0
for _map, robots in TEST_CASES:
    start_time = time.time()
    test_case += 1
    _map = np.array([list(l) for l in _map.split('\n')])
    solution_part1 = HC_1NB_CELLS(_map)
    apply_to_map(_map, solution_part1)

    solution_part2 = DO_MONTE_CARLO(_map, robots, start_time)
    apply_to_map(_map, solution_part2)

    score = calc_score(_map, robots)
    total_score += score
    print(f'TEST CASE {test_case}: {score}')

print(f'-------------------')
print(f'TOTAL SCORE {total_score}')