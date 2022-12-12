import re
import time
from collections import deque
from math import prod, lcm
from typing import Deque, List


class Expression:

    def __init__(self, elements: List[int | str]):
        self.elements = elements
        self.mod_memo = {}

    def calculate_value(self, div):
        elements = self.elements
        if div in self.mod_memo:
            e, s = self.mod_memo[div]
            elements = e + elements[s:]

        value = elements[0] % div
        for i in range(1, len(elements), 2):
            o, operand = elements[i], elements[i + 1]
            operand = operand if operand != -1 else value

            if o == '*':
                value = (value * operand) % div
            if o == '+':
                value = (value + operand) % div

        value %= div
        self.mod_memo[div] = [value], len(self.elements)
        return value


class Monkey:

    def __init__(self, items: Deque[Expression], op: str, multiplicand: int | None, div: int, true_throw: int,
                 false_throw: int):
        self.items = items
        self.op = op
        self.div = div
        self.true_throw = true_throw
        self.false_throw = false_throw
        self.inspects = 0
        self.multiplicand = multiplicand

    def add_operation(self, old):
        if self.multiplicand:
            return [self.op, self.multiplicand]

        if self.op == '+':
            return ['+', -1]

        return ['*', -1]

    def calculate_throws(self):
        throws = []
        while self.items:
            expression = self.items.popleft()
            expression.elements += self.add_operation(expression)
            value = expression.calculate_value(self.div)
            throw = self.true_throw if value % self.div == 0 else self.false_throw
            throws.append((expression, throw))

        self.inspects += len(throws)
        return throws

    def __repr__(self):
        return f'monkey items {self.items}'


def get_last_from_split(s):
    return int(s.split(' ')[-1])


def get_input():
    with open('input') as file:
        lines = [line.strip() for line in file]

    monkeys = []
    mod = 1
    for i in range(0, len(lines), 7):
        items = deque([Expression([int(i)]) for i in re.findall(r'[+-]?\d+', lines[i + 1])])
        op = lines[i + 2].split(' ')[-2:]
        multiplicand = int(op[1]) if op[1] != 'old' else None
        div = get_last_from_split(lines[i + 3])
        true_throw = get_last_from_split(lines[i + 4])
        false_throw = get_last_from_split(lines[i + 5])
        mod = lcm(mod, div)
        monkeys.append(Monkey(items, op[0], multiplicand, div, true_throw, false_throw))

    return mod, monkeys


def solve(inp, n, part):
    mod, monkeys = inp

    for r in range(n):
        for i in range(len(monkeys)):
            throws = monkeys[i].calculate_throws()
            for item, throw in throws:
                monkeys[throw].items.append(item)

    return prod(sorted([m.inspects for m in monkeys])[-2:])


_ = get_input()
start = time.time()
# around 2 secs for my puzzle input
print('Part 2:', solve(_, 10_000, 2))
print(time.time() - start)
# print('Part 2:', solve(get_input(), 10_000, 2))
