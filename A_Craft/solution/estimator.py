import numpy as np
from test_cases import TEST_CASES
from world import calc_score

test_case = 0
total_score = 0
for _map, robots in TEST_CASES:
    test_case += 1
    _map = np.array([list(l) for l in _map.split('\n')])
    score = calc_score(_map, robots)
    total_score += score
    print(f'TEST CASE {test_case}: {score}')

print(f'-------------------')
print(f'TOTAL SCORE {total_score}')