import numpy as np
from test_cases import TEST_CASES
from world import calc_score, apply_to_map
from solver import HC_1NB_CELLS, DO_MONTE_CARLO, DO_SPLITTED_MONTE_CARLO, DO_GREED, DO_GREED_DEPTH
import time

test_case = 0
total_score = 0
for _map, robots in TEST_CASES:
    start_time = time.time()
    test_case += 1
    _map = np.array([list(l) for l in _map.split('\n')])
    solution_part1 = HC_1NB_CELLS(_map)
    apply_to_map(_map, solution_part1)

    solution_part3 = DO_GREED_DEPTH(_map, robots)
    solution_part4 = DO_GREED(_map, robots)

    _tmp_map = np.copy(_map)
    apply_to_map(_tmp_map, solution_part3)
    score3 = calc_score(_tmp_map, robots)

    _tmp_map = np.copy(_map)
    apply_to_map(_tmp_map, solution_part4)
    score4 = calc_score(_tmp_map, robots)

    if score4 > score3:
        solution_part3 = solution_part4
        score3 = score4

    solution_part2 = DO_SPLITTED_MONTE_CARLO(_map, robots, start_time, score3)

    apply_to_map(_map, solution_part3)
    apply_to_map(_map, solution_part2)

    score = calc_score(_map, robots)
    total_score += score
    print(f'TEST CASE {test_case}: {score}')

print(f'-------------------')
print(f'TOTAL SCORE {total_score}')