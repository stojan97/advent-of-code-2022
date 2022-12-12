from collections import deque


def get_input():
    with open('input') as file:
        grid = [list(line.strip()) for line in file]

    start, end = (0, 0), (0, 0)
    ends = []

    for i in range(len(grid)):
        for j in range(len(grid[0])):

            if grid[i][j] == 'S':
                grid[i][j] = 'a'
                end = i, j

            if grid[i][j] == 'a':
                ends.append((i, j))

            if grid[i][j] == 'E':
                grid[i][j] = 'z'
                start = i, j

            grid[i][j] = 27 - (ord(grid[i][j]) - 96)

    return start, end, ends, grid


def dirs(pos):
    i, j = pos
    return [(i - 1, j), (i + 1, j), (i, j - 1), (i, j + 1)]


def solve(input):
    start, end, ends, grid = input
    q = deque([start])
    rows = len(grid)
    cols = len(grid[0])
    min_dist = {start: 0}

    while q:
        pos = q.popleft()
        dist = min_dist[pos]

        for p in dirs(pos):
            if p in min_dist:
                continue

            if 0 <= p[0] < rows and 0 <= p[1] < cols and grid[p[0]][p[1]] <= grid[pos[0]][pos[1]] + 1:
                min_dist[p] = dist + 1
                q.append(p)

    return min_dist[end], min(min_dist[e] for e in ends if e in min_dist)


input = get_input()
part1, part2 = solve(input)
print('Part 1:', part1)
print('Part 2:', part2)
