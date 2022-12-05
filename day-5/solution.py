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


def part1(stacks, moves):
    for amount, s1, s2 in moves:
        for i in range(amount):
            stacks[s2 - 1].append(stacks[s1 - 1].pop())

    return ''.join(s[-1] for s in stacks)


def part2(stacks, moves):
    for amount, s1, s2 in moves:
        s1_len = len(stacks[s1 - 1])
        stacks[s2 - 1] += stacks[s1 - 1][s1_len - amount:]
        stacks[s1 - 1] = stacks[s1 - 1][:s1_len - amount]

    return ''.join(s[-1] for s in stacks)


inp = get_input()
print('Part 1:', part1(deepcopy(inp[0]), inp[1]))
print('Part 2:', part2(inp[0], inp[1]))
