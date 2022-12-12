import re
import time
from collections import deque
from math import prod, lcm
from typing import Deque, Callable


class Monkey:

    def __init__(self, items: Deque[int], op: Callable, multiplicand: int | None, div: int, true_throw: int, false_throw: int):
        self.items = items
        self.op = op
        self.div = div
        self.true_throw = true_throw
        self.false_throw = false_throw
        self.inspects = 0
        self.multiplicand = multiplicand

    def operation(self, old):
        m = self.multiplicand if self.multiplicand else old
        return self.op(old, m)

    def calculate_throws(self, part, mod):
        throws = []
        while self.items:
            item = self.items.popleft()
            item = self.operation(item)
            item = item // 3 if part == 1 else item % mod
            throw = self.true_throw if item % self.div == 0 else self.false_throw
            throws.append((item, throw))

        self.inspects += len(throws)
        return throws


def get_last_from_split(s):
    return int(s.split(' ')[-1])

op_resolve = {
    '*': lambda x, y: x * y,
    '+': lambda x, y: x + y
}
def get_input():
    with open('input') as file:
        lines = [line.strip() for line in file]

    monkeys = []
    mod = 1
    for i in range(0, len(lines), 7):
        items = deque(map(int, re.findall(r'[+-]?\d+', lines[i + 1])))
        op = lines[i + 2].split(' ')[-2:]
        op_cmd = op_resolve[op[0]]
        multiplicand = int(op[1]) if op[1] != 'old' else None

        div = get_last_from_split(lines[i + 3])
        true_throw = get_last_from_split(lines[i + 4])
        false_throw = get_last_from_split(lines[i + 5])
        mod = lcm(mod, div)
        monkeys.append(Monkey(items, op_cmd, multiplicand, div, true_throw, false_throw))

    return mod, monkeys


def solve(inp, n, part):
    mod, monkeys = inp

    for r in range(n):
        for i in range(len(monkeys)):
            throws = monkeys[i].calculate_throws(part, mod)
            for item, throw in throws:
                monkeys[throw].items.append(item)

    return prod(sorted([m.inspects for m in monkeys])[-2:])


_ = get_input()
print('Part 1:', solve(_, 20, 1))
start = time.time()
print('Part 2:', solve(get_input(), 10_000, 2))
print(time.time() - start)
