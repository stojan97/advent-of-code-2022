import math


def get_input():
    grid = []
    with open('input') as file:
        for line in file:
            grid.append([int(i) for i in line.strip()])

    return grid


get_bounds = lambda x, end: [(0, x), (x + 1, end)]
is_visible_row = lambda i, j, grid, z: not any(grid[x][j] >= grid[i][j] for x in range(z[0], z[1]))
is_visible_col = lambda i, j, grid, z: not any(grid[i][x] >= grid[i][j] for x in range(z[0], z[1]))


def part1(grid):
    size = len(grid)
    total = 4 * (size - 1)

    for i in range(1, size - 1):
        for j in range(1, len(grid[0]) - 1):
            r = any(is_visible_row(i, j, grid, z) for z in get_bounds(i, size))
            c = any(is_visible_col(i, j, grid, z) for z in get_bounds(j, size))
            total += int(r | c)

    return total


def get_row_score():
    t = 1


def get_scenic_score(i, j, grid):
    size = len(grid)
    # top
    s1, s2, s3, s4 = 0, 0, 0, 0
    blocked = False
    for x in range(i - 1, -1, -1):
        if x < 0 or blocked:
            break
        else:
            if grid[x][j] >= grid[i][j]:
                blocked = True
            s1 += 1

    # bot
    blocked = False
    for x in range(i + 1, size):
        if x >= size or blocked:
            break
        else:
            if grid[x][j] >= grid[i][j]:
                blocked = True
            s2 += 1

    # left
    blocked = False
    for x in range(j - 1, -1, -1):
        if x < 0 or blocked:
            break
        else:
            if grid[i][x] >= grid[i][j]:
                blocked = True
            s3 += 1

    # right
    blocked = False
    for x in range(j + 1, size):
        if x >= size or blocked:
            break
        else:
            if grid[i][x] >= grid[i][j]:
                blocked = True
            s4 += 1

    return s1 * s2 * s3 * s4


def part2(grid):
    max_scenic_score = -math.inf

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            score = get_scenic_score(i, j, grid)
            max_scenic_score = max(max_scenic_score, score)

    return max_scenic_score


inp = get_input()
print('Part 1:', part1(inp))
print('Part 2:', part2(inp))
