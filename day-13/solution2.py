from collections import deque


def get_input():
    with open('input') as file:
        lines = [line.strip() for line in file]

    pairs = [(eval(lines[i]), eval(lines[i + 1])) for i in range(0, len(lines), 3)]
    return pairs


def is_in_order(pair1, pair2):
    if pair1 is None or pair2 is None:
        return False

    s = deque([(pair1, pair2, 0)])

    while s:
        popped = s.pop()
        p1, p2, i = popped

        while i < len(p1) or i < len(p2):
            if i >= len(p1):
                return -1

            if i >= len(p2):
                return 1

            v1 = p1[i]
            v2 = p2[i]

            if type(v1) == type(v2) == int:
                if v1 < v2:
                    return -1

                elif v1 > v2:
                    return 1

                i += 1
                continue

            if type(v1) == int:
                v1 = [v1]

            if type(v2) == int:
                v2 = [v2]

            if type(v1) == type(v2) == list:
                s.append((p1, p2, i + 1))
                s.append((v1, v2, 0))
                break

    return 0


def part2(pairs):
    # two pointers solution
    all = []
    for p in pairs:
        all.append(p[0])
        all.append(p[1])

    p1 = sum(is_in_order([[2]], x) > 0 for x in all) + 1
    p2 = sum(is_in_order([[6]], x) > 0 for x in all) + 2
    return p1 * p2


inp = get_input()
print('Part 2:', part2(inp))
