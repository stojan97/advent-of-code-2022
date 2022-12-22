import math
import time
from collections import deque


def get_input():
    cubes = set()
    with open('input') as file:
        for line in file:
            split = line.strip().split(',')
            cubes.add((int(split[0]), int(split[1]), int(split[2])))

    return cubes


def get_adj_cubes(cube):
    x, y, z = cube
    return [(x - 1, y, z), (x + 1, y, z), (x, y + 1, z), (x, y - 1, z), (x, y, z + 1), (x, y, z - 1)]


def part1(cubes):
    c = 0
    for cube in cubes:
        for adj_cube in get_adj_cubes(cube):
            if adj_cube not in cubes:
                c += 1

    return c


def inside(cube, bounds):
    x = bounds[0][0] <= cube[0] <= bounds[0][1]
    y = bounds[1][0] <= cube[1] <= bounds[1][1]
    z = bounds[2][0] <= cube[2] <= bounds[2][1]
    return x and y and z


def find_trapped(cube, cubes, trapped, bounds):
    stack = deque([])
    stack.append(cube)
    vis = set()

    while stack:
        top = stack.pop()
        if not inside(top, bounds):
            return True, vis

        vis.add(top)

        for adj_cube in get_adj_cubes(top):
            if adj_cube not in cubes and adj_cube not in vis and adj_cube not in trapped:
                stack.append(adj_cube)

    return False, vis


def part2(cubes):
    trapped = set()
    free_air = set()
    bounds = [[math.inf, -math.inf], [math.inf, -math.inf], [math.inf, -math.inf]]
    for cube in cubes:
        # x
        bounds[0][0] = min(bounds[0][0], cube[0])
        bounds[0][1] = max(bounds[0][1], cube[0])
        # y
        bounds[1][0] = min(bounds[1][0], cube[1])
        bounds[1][1] = max(bounds[1][1], cube[1])
        # z
        bounds[2][0] = min(bounds[2][0], cube[2])
        bounds[2][1] = max(bounds[2][1], cube[2])

    for cube in cubes:
        for adj_cube in get_adj_cubes(cube):
            if adj_cube not in cubes and adj_cube not in free_air:
                is_free, s = find_trapped(adj_cube, cubes, trapped, bounds)
                if is_free:
                    free_air |= s
                else:
                    trapped |= s

    t = 0
    for cube in cubes:
        for adj_cube in get_adj_cubes(cube):
            if adj_cube not in cubes and adj_cube not in trapped:
                t += 1

    return t


inp = get_input()
print('Part 1:', part1(inp))
start = time.time()
print('Part 2:', part2(inp))
print(time.time() - start)
