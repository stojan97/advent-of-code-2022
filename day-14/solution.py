def comp(a, b):
    if a == b:
        return 0
    if a < b:
        return 1
    return -1


def prepare_rocks():
    patterns = []
    with open('input') as file:
        for line in file:
            split = line.strip().split('->')
            pattern = []
            for each in split:
                coordinate = each.strip().split(',')
                pattern.append((int(coordinate[0]), int(coordinate[1])))

            patterns.append(pattern)

    rocks = set()

    for pattern in patterns:
        for c1, c2 in zip(pattern, pattern[1:]):

            while c1 != c2:
                rocks.add(c1)
                c1 = (c1[0] + comp(c1[0], c2[0]), c1[1] + comp(c1[1], c2[1]))

            rocks.add(c1)

    return rocks


def next_cells(x, y):
    return [(x, y + 1), (x - 1, y + 1), (x + 1, y + 1)]


def get_next(current, rocks, sand):
    for cell in next_cells(current[0], current[1]):
        if cell not in rocks and cell not in sand:
            return cell

    return None


def get_simulation_sand(last_row, rocks):
    sand = set()

    while True:
        current = (500, 0)

        while True:
            if current[1] == last_row:
                return len(sand)

            next = get_next(current, rocks, sand)
            if not next:
                break
            current = next

        sand.add(current)


def part1(rocks):
    last_row = max(k[1] for k in rocks)
    return get_simulation_sand(last_row, rocks)


def inside(i, prev_row):
    return (500 - prev_row) <= i <= (500 + prev_row)


def not_covered_by_rocks(point, rocks):
    col, row = point
    row -= 1

    is_not_covered = any((i, row) not in rocks and inside(i, row) for i in range(col - 1, col + 2))
    if not is_not_covered:
        # count covered air as rocks
        rocks.add((col, row + 1))

    return is_not_covered


def should_count(i, j, rocks):
    return (i, j) not in rocks and not_covered_by_rocks((i, j), rocks)


def part2(rocks):
    # using pascal triangle
    last_row = max(k[1] for k in rocks) + 2
    c = 1
    for j in range(1, last_row):
        c += sum(int(should_count(i, j, rocks)) for i in range(500 - j, 500 + j + 1))

    return c


rocks = prepare_rocks()
print('Part 1:', part1(rocks))
print('Part 2:', part2(rocks))
