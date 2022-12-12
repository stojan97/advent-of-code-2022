import math
from collections import deque


def get_input():
    with open('input') as file:
        grid = [list(line.strip()) for line in file]

    start, end = (0, 0), (0, 0)

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 'S':
                grid[i][j] = 'a'
                start = i, j

            if grid[i][j] == 'E':
                grid[i][j] = 'z'
                end = i, j

            grid[i][j] = ord(grid[i][j]) - 96

    for i in range(1, 27):
        LETTERS.append(chr(i + 96))

    return start, end, grid


LETTERS = []


def dirs(pos):
    i, j = pos
    return [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]


def fewest_steps(start, end, grid):
    q = deque([(start, 0)])
    rows = len(grid)
    cols = len(grid[0])
    visited = set()
    visited.add(start)

    while q:
        pos, dist = q.popleft()
        if pos == end:
            return dist

        for p in dirs(pos):
            if p in visited:
                continue

            if 0 <= p[0] < rows and 0 <= p[1] < cols and grid[p[0]][p[1]] <= grid[pos[0]][pos[1]] + 1:
                visited.add(p)
                q.append((p, dist + 1))

    return math.inf


def part1(input):
    start, end, grid = input
    return fewest_steps(start, end, grid)


def part2(input):
    start, end, grid = input
    fewest = math.inf

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == 1:
                fewest = min(fewest, fewest_steps((i, j), end, grid))

    return fewest


input = get_input()
print('Part 1:', part1(input))
print('Part 2:', part2(input))
