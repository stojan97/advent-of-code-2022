import math
from typing import List, Union


class TreeNode:

    def __init__(self, name: str, type: str, children: Union[List['TreeNode'], None], parent: Union['TreeNode', None],
                 size: int = 0) -> None:
        self.name = name
        self.type = type
        self.children = children
        self.size = size
        self.parent = parent


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
                    node.children.append(TreeNode(line[1], 'file', None, node, int(line[0])))
                else:
                    node.children.append(TreeNode(line[1], 'dir', [], node))

    def calculate_size(node):
        if node.type == 'dir':
            node.size = sum(calculate_size(child) for child in node.children)

        return node.size

    calculate_size(tree)
    return tree


def get_size(node):
    t = sum(get_size(child) for child in node.children if child.type == 'dir')
    return node.size + t if node.size <= 100_000 else t


def min_disk_space_to_delete(node, rem):
    children = [min_disk_space_to_delete(child, rem) for child in node.children if child.type == 'dir']
    min_child = min(children) if len(children) > 0 else math.inf
    current = node.size if node.size >= rem else math.inf
    return min(current, min_child)


def part1(tree):
    return get_size(tree)


def part2(tree):
    rem = 30_000_000 - (70_000_000 - tree.size)
    return min_disk_space_to_delete(tree, rem)


tree = get_input()
print('Part 1:', part1(tree))
print('Part 2:', part2(tree))
