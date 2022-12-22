def get_input():
    with open('input') as file:
        lines = [line.strip() for line in file]

    return lines[0]


def check_all_can_move(shape, op, rocks):
    for s in shape:
        next = op(s)
        if next in rocks or not (0 <= next[1] <= 6):
            return False
    return True


def part1(moves):

    shapes = [
        lambda x: [(x, i) for i in range(2, 6)],  # -
        lambda x: [(x + 2, 3)] + [(x + 1, i) for i in range(2, 5)] + [(x, 3)],  # +
        lambda x: [(x + 2, 4)] + [(x + 1, 4)] + [(x, i) for i in range(2, 5)],  #
        lambda x: [(x + i, 2) for i in range(4)],
        lambda x: [(x + 1, i) for i in range(2, 4)] + [(x, i) for i in range(2, 4)],
    ]

    index = 0
    stopped_falling = 0
    rocks = set()

    for y in range(7):
        rocks.add((0, y))

    max_unit = 0

    dir = {
        'v': lambda s: (s[0] - 1, s[1]),
        '<': lambda s: (s[0], s[1] - 1),
        '>': lambda s: (s[0], s[1] + 1)
    }

    shape = None
    switch_shape = True
    move_index = 0

    while True:
        if stopped_falling == 2022:
            break

        can_move_down = 0
        # move to left/right
        if switch_shape:
            shape = shapes[index](max_unit + 4)
            switch_shape = False

        op = dir[moves[move_index]]
        move_index = (move_index + 1) % len(moves)

        if check_all_can_move(shape, op, rocks):
            shape = [op(s) for s in shape]
        # move down
        op = dir['v']
        if check_all_can_move(shape, op, rocks):
            shape = [op(s) for s in shape]
            can_move_down += 1

        if can_move_down == 0:
            max_height = max(shape, key=lambda z: z[0])[0]
            max_unit = max(max_unit, max_height)
            rocks |= set(shape)
            stopped_falling += 1
            index = (index + 1) % 5
            switch_shape = True

    return max_unit


def part2(moves):
    shapes = [
        lambda x: [(x, i) for i in range(2, 6)],  # -
        lambda x: [(x + 2, 3)] + [(x + 1, i) for i in range(2, 5)] + [(x, 3)],  # +
        lambda x: [(x + 2, 4)] + [(x + 1, 4)] + [(x, i) for i in range(2, 5)],  # J
        lambda x: [(x + i, 2) for i in range(4)], # |
        lambda x: [(x + 1, i) for i in range(2, 4)] + [(x, i) for i in range(2, 4)], # #
    ]

    shape_image = ['-', '+', 'J', '|', '#']

    index = 0
    rocks = set()

    for y in range(7):
        rocks.add((0, y))

    max_unit = 0

    dir = {
        'v': lambda s: (s[0] - 1, s[1]),
        '<': lambda s: (s[0], s[1] - 1),
        '>': lambda s: (s[0], s[1] + 1)
    }

    shape = None
    switch_shape = True
    period = len(moves)
    move_index = 0
    last = 1000000000000
    max_falling_shape = (last - 1) % 5
    limit = last - 1
    shape_limit = (limit // 5) + 1
    last_shape_move_index = 0
    res = []
    last_height = 0
    s1 = 0
    # for all shapes there is period +x height
    stopped_shapes = 0
    inside_period = False
    init_period_shape_diff = 0
    period_height = 0

    while True:
        can_move_down = 0
        # move to left/right
        if switch_shape:
            shape = shapes[index](max_unit + 4)
            switch_shape = False

        op = dir[moves[move_index % period]]
        move_index = (move_index + 1)

        if check_all_can_move(shape, op, rocks):
            shape = [op(s) for s in shape]
        # move down
        op = dir['v']
        if check_all_can_move(shape, op, rocks):
            shape = [op(s) for s in shape]
            can_move_down += 1

        if can_move_down == 0:
            max_height = max(shape, key=lambda z: z[0])[0]
            max_unit = max(max_unit, max_height)
            rocks |= set(shape)
            stopped_shapes += 1
            if shape_image[index] == shape_image[max_falling_shape]:
                s1 += 1
                last_shape_move_index = move_index - 1
                if inside_period and last_shape_move_index < period * 2:
                    res.append(res[-1] + (max_unit - last_height))
                    last_height = max_unit

            index = (index + 1) % 5
            switch_shape = True

        if last_shape_move_index > period and not inside_period:
            res = [max_unit]
            last_height = max_unit
            init_period_shape_diff = s1
            inside_period = True

        if last_shape_move_index > period * 2 and period_height == 0:
            assert len(res) >= 1
            period_height = max_unit - res[0]
            period_shape_diff = s1 - init_period_shape_diff
            break

    shape_limit -= init_period_shape_diff
    mul_by_period_height = (shape_limit // period_shape_diff)
    loc = shape_limit % period_shape_diff
    mul_height = mul_by_period_height * period_height
    return res[loc] + mul_height


inp = get_input()
print('Part 1:', part1(inp))
print('Part 2:', part2(inp))
