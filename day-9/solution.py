def get_input():
    with open('input') as file:
        moves = [(line.strip().split()[0], int(line.strip().split()[1])) for line in file]

    return moves


move = {
    'L': lambda head: (head[0], head[1] - 1),
    'R': lambda head: (head[0], head[1] + 1),
    'U': lambda head: (head[0] - 1, head[1]),
    'D': lambda head: (head[0] + 1, head[1]),
}


def add_opposite_one(x):
    return -(x // abs(x)) if x != 0 else 0


def adjust_tail(front, current):
    diff_x = front[0] - current[0]
    diff_y = front[1] - current[1]

    if abs(diff_x) == 2 and abs(diff_y) == 1:
        diff_y *= 2

    if abs(diff_x) == 1 and abs(diff_y) == 2:
        diff_x *= 2

    diff_x += add_opposite_one(diff_x)
    diff_y += add_opposite_one(diff_y)

    return current[0] + diff_x, current[1] + diff_y


def get_simulation_result(moves, knots):
    res = set()
    res.add((0, 0))

    for d, steps in moves:
        for i in range(steps):
            knots[0] = move[d](knots[0])

            for j in range(1, len(knots)):
                knots[j] = adjust_tail(knots[j - 1], knots[j])

            res.add(knots[-1])

    return len(res)


def solve(moves, k):
    knots = [(0, 0) for _ in range(k)]
    return get_simulation_result(moves, knots)


inp = get_input()
print('Part 1:', solve(inp, 2))
print('Part 2:', solve(inp, 10))
