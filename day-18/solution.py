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


def find_trapped(cube, cubes, surface_area, trapped, free_air):
    stack = deque([])
    stack.append(cube)
    vis = set()

    while stack:
        top = stack.pop()
        if len(stack) >= surface_area:
            return True, vis

        vis.add(top)

        for adj_cube in get_adj_cubes(top):
            if adj_cube not in cubes and adj_cube not in vis and adj_cube not in trapped:
                stack.append(adj_cube)

    return False, vis

def part2(cubes):
    surface_area = part1(cubes)
    trapped = set()
    free_air = set()

    for cube in cubes:
        for adj_cube in get_adj_cubes(cube):
            if adj_cube not in cubes and adj_cube not in free_air:
                is_free, s = find_trapped(adj_cube, cubes, surface_area, trapped, free_air)
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
