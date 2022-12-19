def get_input():
    with open('input') as file:
        lines = [line.strip() for line in file]

    print(lines)
    return lines


def part1(input):

    # -, +, L, |, # - see there starting pos and simulate
    # shapes start 4 rows higher from the last fall
    # calculate after 2022 rocks, the units tall (vertical spread)
    # How to represent rocks?
    # cells, move each cell every round
    # right move (right -> left move cells), left move (left -> right move cells)
    # bottom move (bottom -> top move cells)
    # [x,y] [x,y+1]
    #       [x+1,y+1]
    pass


def part2(input):
    pass


inp = get_input()
print('Part 1:', part1(inp))
print('Part 2:', part2(inp))
