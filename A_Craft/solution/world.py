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