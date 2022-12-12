import re
import time
from collections import deque
from math import prod
from typing import Deque, Callable, List


class Monkey:

    def __init__(self, index: int, items: Deque[int], op: Callable, multiplicand: int | None, div: int, true_throw: int,
                 false_throw: int):
        self.index = index
        self.items = items
        self.op = op
        self.div = div
        self.true_throw = true_throw
        self.false_throw = false_throw
        self.inspects = 0
        self.multiplicand = multiplicand
        self.items_mods: Deque[List[int]] = deque([])

    def operation(self, old):
        m = self.multiplicand if self.multiplicand else old
        return self.op(old, m)

    def calculate_throws(self, mods):
        throws = []
        while self.items_mods:
            item_mod_list = self.items_mods.popleft()
            for z in range(len(item_mod_list)):
                item_mod_list[z] = self.operation(item_mod_list[z])
                item_mod_list[z] %= mods[z]

            throw = self.true_throw if item_mod_list[self.index] == 0 else self.false_throw
            throws.append((item_mod_list, throw))

        self.inspects += len(throws)
        return throws

    def __repr__(self):
        return f'{self.inspects}'


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
    mods = []
    index = 0
    for i in range(0, len(lines), 7):
        items = deque(map(int, re.findall(r'[+-]?\d+', lines[i + 1])))
        op = lines[i + 2].split(' ')[-2:]
        op_cmd = op_resolve[op[0]]
        multiplicand = int(op[1]) if op[1] != 'old' else None

        div = get_last_from_split(lines[i + 3])
        mods.append(div)
        true_throw = get_last_from_split(lines[i + 4])
        false_throw = get_last_from_split(lines[i + 5])
        monkeys.append(Monkey(index, items, op_cmd, multiplicand, div, true_throw, false_throw))
        index += 1

    for monkey in monkeys:
        for monkey_item in monkey.items:
            monkey.items_mods.append([monkey_item % m for m in mods])

    return mods, monkeys


def solve(inp, n):
    mods, monkeys = inp

    for r in range(n):
        for i in range(len(monkeys)):
            throws = monkeys[i].calculate_throws(mods)
            for item_mod_list, throw in throws:
                monkeys[throw].items_mods.append(item_mod_list)

    return prod(sorted([m.inspects for m in monkeys])[-2:])


start = time.time()
print('Part 2:', solve(get_input(), 10_000))
print(time.time() - start)
