import time


class Node:
    def __init__(self, value):
        self.value = value

    def __repr__(self):
        return f'{self.value}'


def get_input():
    with open('input') as file:
        arrangement = [int(line.strip()) for line in file]

    llist = []
    init = []
    zero_node = None

    for i in range(len(arrangement)):
        node = Node(arrangement[i])
        if arrangement[i] == 0:
            zero_node = node
        llist.append(node)
        init.append(node)

    return llist, init, zero_node


def do_movement(llist, init, MOD):
    for i in range(len(llist)):
        node = init[i]
        node_index = llist.index(node)
        last_pos = (node_index + node.value) % (MOD - 1)
        slice = llist[:node_index] + llist[node_index + 1:]
        llist = slice[:last_pos] + [node] + slice[last_pos:]

    return llist


def part1(llist, init, zero_node):
    MOD = len(llist)
    llist = do_movement(llist, init, MOD)
    zero_node_index = llist.index(zero_node)
    return sum(llist[(zero_node_index + idx) % MOD].value for idx in [1000, 2000, 3000])


def part2(llist, init, zero_node):
    MOD = len(llist)

    key = 811589153

    for i in range(len(llist)):
        llist[i].value *= key

    for round in range(10):
        print(f'========== {round + 1} ==========')
        llist = do_movement(llist, init, MOD)

    zero_node_index = llist.index(zero_node)
    return sum(llist[(zero_node_index + idx) % MOD].value for idx in [1000, 2000, 3000])


llist, init, zero_node = get_input()
print('Part 1:', part1(llist, init, zero_node))
start = time.time()
# 5 secs part 2
print('Part 2:', part2(llist, init, zero_node))
print(time.time() - start)
