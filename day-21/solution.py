def get_input():
    OPS1 = {
        '+': lambda a, b: a + b,
        '-': lambda a, b: a - b,
        '*': lambda a, b: a * b,
        '/': lambda a, b: a // b
    }

    OPS2 = {
        '+': lambda a, b: f'({a} + {b})',
        '-': lambda a, b: f'({a} - {b})',
        '*': lambda a, b: f'({a} * {b})',
        '/': lambda a, b: f'({a} / {b})',
    }

    monkeys = {}
    with open('input') as file:
        for line in file:

            split = line.strip().split(': ')
            if split[1].isnumeric():
                monkey_number = (True, int(split[1]))
            else:
                exp = split[1].split(' ')
                op1 = OPS1[exp[1]]
                op2 = OPS2[exp[1]]
                monkey_number = (False, op1, op2, exp[0], exp[2])

            monkeys[split[0]] = monkey_number

    return monkeys


def get_monkey_number(monkey, monkeys):
    monkey_number = monkeys[monkey]
    if monkey_number[0]:
        return monkey_number[1]

    _, op, _, a, b = monkey_number
    number = op(get_monkey_number(a, monkeys), get_monkey_number(b, monkeys))
    return number


def part1(monkeys):
    return get_monkey_number('root', monkeys)


def expand_expression(monkey, monkeys):
    monkey_number = monkeys[monkey]

    if monkey == 'humn':
        return 'j'

    if monkey_number[0]:
        return monkey_number[1]

    _, _, op, a, b = monkey_number
    expression_a = expand_expression(a, monkeys)
    expression_b = expand_expression(b, monkeys)
    return op(expression_a, expression_b)


def part2(monkeys):
    root = monkeys['root']
    monkeys['root'] = False, None, lambda a, b: f'{a} - {b}', root[3], root[4]
    expression = expand_expression('root', monkeys)
    solution = eval(expression, {'j': 1j})
    # ax + b = 0 => x = -b/a
    ans = int(solution.real / -solution.imag)
    return ans

inp = get_input()
print('Part 1:', part1(inp))
print('Part 2:', part2(inp))
