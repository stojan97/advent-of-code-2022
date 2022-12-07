import math
from typing import List, Union


class TreeNode:

    def __init__(self, name: str, type: str, children: List['TreeNode'], parent: Union['TreeNode', None],
                 size: int = 0) -> None:
        self.name = name
        self.type = type
        self.children = children
        self.size = size
        self.parent = parent

    def calculate_size(self):
        self.size += sum(child.calculate_size() for child in self.children)
        return self.size

    def get_size_at_most(self, at_most):
        t = sum(child.get_size_at_most(at_most) for child in self.children if child.type == 'dir')
        return self.size + t if self.size <= at_most else t

    def min_disk_space_to_delete(self, rem):
        children = [child.min_disk_space_to_delete(rem) for child in self.children if child.type == 'dir']
        min_child = min(children) if len(children) > 0 else math.inf
        current = self.size if self.size >= rem else math.inf
        return min(current, min_child)


def get_input():
    tree = TreeNode('/', 'dir', [], None)
    node = tree

    with open('input') as file:

        for line in file:
            line = line.strip().split()

            if line[0] == '$':
                if line[1] == 'cd':
                    if line[2] == '/':
                        continue

                    if line[2] == '..':
                        node = node.parent
                        continue

                    next_node = next((c for c in node.children if c.name == line[2]), None)
                    if not next_node:
                        next_node = TreeNode(line[2], 'dir', [], node)
                        node.children.append(next_node)

                    node = next_node

            else:
                if line[0].isnumeric():
                    node.children.append(TreeNode(line[1], 'file', [], node, int(line[0])))
                else:
                    node.children.append(TreeNode(line[1], 'dir', [], node))

    tree.calculate_size()
    return tree


def part1(tree):
    return tree.get_size_at_most(100_000)


def part2(tree):
    rem = 30_000_000 - (70_000_000 - tree.size)
    return tree.min_disk_space_to_delete(rem)


tree = get_input()
print('Part 1:', part1(tree))
print('Part 2:', part2(tree))
