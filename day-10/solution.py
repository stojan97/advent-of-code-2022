def get_input():
    with open('input') as file:
        lines = [line.strip().split(' ') for line in file]

    return lines


def add_total(x, cycle):
    return x * cycle if cycle % 40 == 20 else 0


def add_new_line(cycle):
    return '\n' if cycle % 40 == 1 and cycle > 40 else ''


def resolve_pixel(x, cycle):
    return '#' if (cycle - 1) % 40 in [x - 1, x, x + 1] else ' '


def perform_operation(crt, cycle, total, x):
    total += add_total(x, cycle)
    crt += add_new_line(cycle)
    crt += resolve_pixel(x, cycle)
    return crt, total, cycle


def solve(instructions):
    x = 1
    cycle = 0
    total = 0
    crt = ''

    for ins in instructions:
        crt, total, cycle = perform_operation(crt, cycle + 1, total, x)

        if ins[0] == 'addx':
            crt, total, cycle = perform_operation(crt, cycle + 1, total, x)
            x += int(ins[1])

    return total, crt


inp = get_input()
part1, part2 = solve(inp)
print('Part 1:', part1)
print('Part 2:')
print(part2)
