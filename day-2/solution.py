def get_input():
    with open('input') as file:
        lines = [('ABC'.index(line.split()[0]), 'XYZ'.index(line.split()[1])) for line in file]
    return lines


def part1(input):
    total = 0
    for first, second in input:
        total += second + 1
        if first == second:
            total += 3
        if first == (second + 2) % 3:
            total += 6

    return total


def part2(input):
    total = 0
    shift_to_strategy = [2, 0, 1]
    for first, second in input:
        total += 3 * second
        total += ((first + shift_to_strategy[second]) % 3) + 1

    return total


inp = get_input()
print('Part 1:', part1(inp))
print('Part 2:', part2(inp))
