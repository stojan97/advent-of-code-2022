import re
import time
from copy import copy


# class Blueprint:
#     def __init__(self, id, robots, coins, costs):
#         self.id = id
#         self.robots = robots
#         self.coins = coins
#         self.costs = costs
#
#     def __repr__(self):
#         return f'Blueprint id={self.id}, robots={self.robots}, coins={self.coins}, costs={self.costs}'
#

def get_numbers(str):
    return list(map(int, re.findall(r'\d+', str)))


def get_input():
    blueprints = []
    with open('input') as file:
        id = 1
        for line in file:
            # 0 - ore
            # 1 - clay
            # 2 - obsidian
            # 3 - geode
            strip = line.strip().split('. ')
            costs = [0, 0, 0, 0]
            ore_costs = get_numbers(strip[0].split('Each ')[1])
            print(ore_costs)
            costs[0] = {0: ore_costs[0]}
            clay_costs = get_numbers(strip[1].split('Each ')[1])
            print(clay_costs)
            costs[1] = {0: clay_costs[0]}
            obsidian_costs = get_numbers(strip[2].split('Each ')[1])
            print(obsidian_costs)
            costs[2] = {0: obsidian_costs[0], 1: obsidian_costs[1]}
            geode_costs = get_numbers(strip[3].split('Each ')[1])
            print(geode_costs)
            costs[3] = {0: geode_costs[0], 2: geode_costs[1]}

            blueprint = (id, (1, 0, 0, 0), (0, 0, 0, 0), costs)
            print(blueprint)
            blueprints.append(blueprint)
            id += 1
            print()

    return blueprints


def possible_to_build_robot(cost, coins):
    for coin, c in cost.items():
        if coins[coin] < c:
            return False

    return True


def next_value(val, r_i, i):
    return val + int(r_i == i)


def d_cost(val, i, cost):
    return val - cost[i] if i in cost else val


def get_next_state(i, robots, new_coins, cost):
    robots = (
        next_value(robots[0], 0, i),
        next_value(robots[1], 1, i),
        next_value(robots[2], 2, i),
        next_value(robots[3], 3, i)
    )
    new_coins = (
        d_cost(new_coins[0], 0, cost),
        d_cost(new_coins[1], 1, cost),
        d_cost(new_coins[2], 2, cost),
        d_cost(new_coins[3], 3, cost)
    )

    return robots, new_coins

id = 1

def get_max_geode(state, dp):
    robots, coins, costs, time = state
    memo = robots, coins, time

    if memo in dp:
        global id
        if id % 100_000 == 0:
            print(f'hits={id} === State={memo}, dp={len(dp)}')
        id += 1
        return dp[memo]
    # global id
    # if id % 100_000 == 0:
    #     print(f'hits={id} === State={memo}, dp={len(dp)}')
    # id += 1

    # collect coins
    new_coins = (coins[0] + robots[0], coins[1] + robots[1], coins[2] + robots[2], coins[3] + robots[3])
    init_geode = new_coins[3]
    ans = init_geode

    if time == 24:
        dp[memo] = ans
        return ans

    ans = max(ans, get_max_geode((robots, new_coins, costs, time + 1), dp))

    for i in range(len(robots)):
        # check if robot is possible to be built
        if possible_to_build_robot(costs[i], coins) and costs[i] :
            r, c = get_next_state(i, robots, new_coins, costs[i])
            ans = max(ans, get_max_geode((r, c, costs, time + 1), dp))

    dp[memo] = ans
    return ans


def part1(blueprints):
    s = 0

    # Approach 1:
    # shortest path to reach some target geode state (1,4,2,[2])
    # PQ (heap) for minimum minutes
    # Binary search the answer?

    # Approach 2:
    # Blueprint 1:
    # Each ore robot costs 4 ore.
    # Each clay robot costs 2 ore.
    # Each obsidian robot costs 3 ore and 14 clay.
    # Each geode robot costs 2 ore => 3min (1 ore + 1 min create ore-robot, 1 min 2 ore) 1 ore rem -> 3min
    # 7 obsidian -> 3 ore - 1 = 2 ore :::::: 14 clay

    for blueprint in blueprints[:1]:
        dp = {}
        geode = get_max_geode((blueprint[1], blueprint[2], blueprint[3], 1), dp)
        quality = blueprint[0] * geode
        print(f'Blueprint {blueprint[0]}: {geode} => {quality}')
        s += quality

    return s


def part2(input):
    pass


inp = get_input()
start = time.time()
print('Part 1:', part1(inp))
print(time.time() - start)
# print('Part 2:', part2(inp))
