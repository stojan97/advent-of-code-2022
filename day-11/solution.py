import re
from collections import deque
from math import prod, lcm
from typing import Deque


class Monkey:

    def __init__(self, items: Deque[int], op: str, div: int, true_throw: int, false_throw: int):
        self.items = items
        self.op = op
        self.div = div
        self.true_throw = true_throw
        self.false_throw = false_throw
        self.inspects = 0

    def operation(self, old):
        return eval(self.op)

    def calculate_throw(self, do_additional_operation, mod):
        throws = []
        while self.items:
            item = self.items.popleft()
            item = self.operation(item)
            item = do_additional_operation(item, mod)
            throw = self.true_throw if item % self.div == 0 else self.false_throw
            throws.append((item, throw))

        self.inspects += len(throws)
        return throws


def get_last_from_split(s):
    return int(s.split(' ')[-1])


def get_input():
    with open('input') as file:
        lines = [line.strip() for line in file]

    monkeys = []
    mod = 1
    for i in range(0, len(lines), 7):
        items = deque(map(int, re.findall(r'[+-]?\d+', lines[i + 1])))
        op = 'old' + ''.join(lines[i + 2].split(' ')[-2:])
        div = get_last_from_split(lines[i + 3])
        true_throw = get_last_from_split(lines[i + 4])
        false_throw = get_last_from_split(lines[i + 5])
        mod = lcm(mod, div)
        monkeys.append(Monkey(items, op, div, true_throw, false_throw))

    return mod, monkeys


def solve(inp, n, do_additional_operation):
    mod, monkeys = inp

    for r in range(n):
        for i in range(len(monkeys)):
            throws = monkeys[i].calculate_throw(do_additional_operation, mod)
            for item, throw in throws:
                monkeys[throw].items.append(item)

    return prod(sorted([m.inspects for m in monkeys])[-2:])


print('Part 1:', solve(get_input(), 20, lambda i, mod: i // 3))
print('Part 2:', solve(get_input(), 10_000, lambda i, mod: i % mod))
