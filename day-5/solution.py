import re
from copy import deepcopy


def get_input():
    moves = []
    lines = []
    is_move = False
    n_stacks = 0

    with open('input') as file:
        for line in file:
            str_line = line.strip()
            numbers = re.findall(r'\d+', str_line)
            if is_move:
                moves.append(tuple(map(int, numbers)))
                continue

            if not str_line:
                is_move = True
                continue

            if len(numbers) > 0:
                n_stacks = len(numbers)
                continue

            chunked_stacks = ''.join(line[i + 1] for i in range(0, len(line), 4))

            lines.append(chunked_stacks)

    stacks = [[] for _ in range(n_stacks)]

    for line in reversed(lines):
        for i in range(len(line)):
            if line[i].isalpha():
                stacks[i].append(line[i])

    return stacks, moves


def solve(stacks, moves, to_reverse):
    for amount, s1, s2 in moves:
        stacks[s2 - 1] += to_reverse(stacks[s1 - 1][-amount:])
        stacks[s1 - 1] = stacks[s1 - 1][:-amount]

    return ''.join(s[-1] for s in stacks)


inp = get_input()
print('Part 1:', solve(deepcopy(inp[0]), inp[1], lambda s: reversed(s)))
print('Part 2:', solve(inp[0], inp[1], lambda s: s))
