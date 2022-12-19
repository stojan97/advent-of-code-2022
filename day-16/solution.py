import math
import re
import time
from collections import deque
from heapq import heappop, heappush, heapify
from itertools import permutations, product


def shortest_path_to_other_for_valve(valve, graph):
    pq = [(0, valve, '')]
    heapify(pq)
    visited = set()
    d = {v: math.inf for v in graph.keys()}
    d[valve] = 0

    while pq:
        dist, current_valve, path = heappop(pq)

        if current_valve in visited:
            continue

        visited.add(current_valve)

        for v in graph[current_valve][1]:
            next_dist = dist + 1
            if next_dist < d[v]:
                d[v] = next_dist
                heappush(pq, (next_dist, v, path))

    return valve, d['AA'], d


def get_input():
    graph = {}
    with open('input') as file:
        for line in file:
            split = line.strip().split()
            node = split[1]
            flow = int(re.findall(r'[+-]?\d+', split[4])[0])
            adj = [i.split(',')[0] for i in split[9:]]
            graph[node] = (flow, adj)

    # init planar graph
    shortest_paths = []
    map_to_idx = {}

    idx = 0
    # find the shortest path for each node with flow rate
    for key, value in graph.items():
        if value[0] != 0:
            shortest_paths.append(shortest_path_to_other_for_valve(key, graph))
            map_to_idx[key] = idx
            idx += 1

    # map node -> index in final graph
    final_graph = []
    for i in range(len(shortest_paths)):
        adj = []
        valve = shortest_paths[i][0]
        start_time = shortest_paths[i][1]
        min_dist = shortest_paths[i][2]
        pressure = graph[valve][0]
        for v, j in map_to_idx.items():
            if i != j and min_dist[v] != math.inf:
                adj.append((j, min_dist[v] + 1))

        final_graph.append((valve, start_time + 1, pressure, adj))

    print('Graph length', len(final_graph))
    return graph, map_to_idx, final_graph


def find_max_remaining_cost_p1(current, graph):
    idx, time, time_spent, pressure, bitmask = current

    flow = time_spent * pressure
    pressure += graph[idx][2]

    ans = flow + (30 - time) * pressure

    # visit adj
    for i, t in graph[idx][3]:
        next_time = time + t
        if not (bitmask & (1 << i)) and next_time <= 30:
            ans = max(ans,
                      flow + find_max_remaining_cost_p1((i, next_time, t, pressure, bitmask | 1 << i), graph))

    return ans


def part1(graph):
    mask = 1 << len(graph)
    ans = 0
    for idx, node in enumerate(graph):
        ans = max(ans, find_max_remaining_cost_p1((idx, node[1], node[1], 0, mask | 1 << idx, ''), graph))

    return ans


id = 0
az = 0


def find_max_remaining_cost(current, graph, dp):
    p_idx, e_idx, time, time_left, pressure, rem_p, rem_e, bitmask_covered = current

    memo = (p_idx, e_idx, time_left, bitmask_covered)

    global id
    global az

    # flow until this minute
    flow = time_left * pressure

    if memo in dp:
        if id % 500_000 == 0:
            print(f'DP HIT {id} :: size={len(dp)}, ans={az}')
        id += 1
        return dp[memo]

    person_opens = p_idx is not None and rem_p == 0
    elephant_opens = e_idx is not None and rem_e == 0

    # calculate pressure for next flow

    if person_opens:
        pressure += graph[p_idx][2]

    if elephant_opens:
        pressure += graph[e_idx][2]

    # calculate until the end the next pressure
    ans = (26 - time) * pressure

    finished = [(None, math.inf)]

    if rem_p > 0:
        person_next = [(p_idx, rem_p)]
    else:
        person_next = [(i, t) for i, t in graph[p_idx][3] if
                       not (bitmask_covered & (1 << i))] if p_idx is not None else []

    if rem_e > 0:
        elephant_next = [(e_idx, rem_e)]
    else:
        elephant_next = [(i, t) for i, t in graph[e_idx][3] if
                         not (bitmask_covered & (1 << i))] if e_idx is not None else []

    if not person_next and not elephant_next:
        ans = flow + ans
        dp[memo] = ans
        az = max(az, ans)
        return ans

    if not person_next:
        person_next = finished

    if not elephant_next:
        elephant_next = finished

    # if path1.startswith('JJ->JJ->BB->CC') and path2.startswith('DD->HH->HH->EE'):
    #     print(person_next, elephant_next)

    for (i, t1), (j, t2) in product(person_next, elephant_next):
        t = min(t1, t2)
        next_time = time + t
        if i != j and next_time <= 26:
            mask_i = (1 << i) if i is not None else 0
            mask_j = (1 << j) if j is not None else 0
            next = (i, j, next_time, t, pressure, t1 - t, t2 - t, bitmask_covered | mask_i | mask_j)
            ans = max(ans, find_max_remaining_cost(next, graph, dp))

    # if path1.startswith('JJ') and path2.startswith('DD'):
    #
    #     print(
    #         f'== Minute {time} RES={app} :: person_path={path1}, elephant_path={path2}, remaining_time_person={rem_p}, remaining_time_elephant={rem_e} flow={flow}, until_26_flow={ans}, pressure={pressure}, bitmask_covered={bitmask_covered}')

    # f(current) = flow + f(adj, t + 1)
    # f(person_node, elephant_node, bitmask, t) = last_node with next set bitmask, at time t
    ans = flow + ans
    dp[memo] = ans
    az = max(az, ans)
    return ans


def min_time(current, graph, dp, map_to_idx):
    p, e, time, pressure, bitmask = current

    memo = (p, e, time, bitmask)

    if time == 9 and p == 'CC' and e == 'FF':
        print(current)

    global id
    global az

    if memo in dp:
        if id % 100_000 == 0:
            print(f'DP HIT {id} :: size={len(dp)}, ans={az}')
        id += 1
        return dp[memo]

    valve_flow_p = graph[p][0]
    adj_p = graph[p][1]

    valve_flow_e = graph[e][0]
    adj_e = graph[e][1]

    person_next = [(i, 0) for i in adj_p]
    elephant_next = [(i, 0) for i in adj_e]

    if valve_flow_p > 0 and not (bitmask & (1 << map_to_idx[p])):
        # open valve in next move
        person_next.append((p, valve_flow_p))

    if valve_flow_e > 0 and not (bitmask & (1 << map_to_idx[e])):
        elephant_next.append((e, valve_flow_e))

    # if path1.startswith('JJ->JJ->BB->CC') and path2.startswith('DD->HH->HH->EE'):
    #     print(person_next, elephant_next)
    ans = 0

    for (i, p1), (j, p2) in product(person_next, elephant_next):

        if i != j and time + 1 <= 26:
            next_pressure = pressure + p1 + p2
            mask_i = 1 << map_to_idx[i] if p1 > 0 else 0
            mask_j = 1 << map_to_idx[j] if p2 > 0 else 0

            next = (i, j, time + 1, next_pressure, bitmask | mask_i | mask_j)
            ans = max(ans, min_time(next, graph, dp, map_to_idx))

    flow = pressure + ans
    az = max(az, flow)
    dp[memo] = flow
    return flow

    # flow, pressure, node, t, bitmask = heappop(pq)

    # if largest_mask == bitmask:
    #     ans = min(ans, flow + (30 - t) * pressure)
    #     # if idx % 100_000 == 0:
    #     #     pass
    #     # print('All valves opened', flow, pressure, ans, idx, node, t, bitmask)
    #     # print(len(q))
    #     # idx += 1
    #     continue
    #
    # if t == 30:
    #     ans = min(ans, flow)
    #     # if idx2 % 100_000 == 0:
    #     #     pass
    #     # print('T == 30', flow, pressure, ans, idx, node, t, bitmask)
    #     # idx2 += 1
    #     # print(len(q))
    #     continue
    #
    # next_flow = flow + pressure
    #
    # valve_flow = graph[node][0]
    # adj = graph[node][1]
    # index = graph[node][2]
    #
    # # open current valve
    # if not (bitmask & (1 << index)):
    #     next_pressure = pressure - valve_flow
    #     # heappush(pq, (next_flow + next_pressure, next_pressure, node, t + 1, bitmask | (1 << index)))
    #     q.append((next_flow, next_pressure, node, t + 1, bitmask | (1 << index)))
    # else:
    #     # move to other valve if the current is open
    #     for next in adj:
    #         # heappush(pq, (next_flow, pressure, next, t + 1, bitmask))
    #         q.append((next_flow, pressure, next, t + 1, bitmask))


def part2(inp):
    graph, map_to_idx, final_graph = inp
    mask = 1 << len(final_graph)
    full_mask = (1 << (len(final_graph) + 1)) - 1
    print(mask, full_mask)
    ans = 0
    print('Graph', graph)
    print('MAP', map_to_idx)

    dp = {}

    # probably t + 1 implementation with dp might work as last resort or matevskial is genius

    # for i, person in enumerate(graph):
    #     for j, elephant in enumerate(graph):
    #         if i != j:
    #             # p_idx, e_idx, time, time_spent, pressure, rem_p, rem_e, bitmask_rem, valve_p, valve_e, path1, path2
    #             t = min(person[1], elephant[1])
    #             cost = find_max_remaining_cost(
    #                 (i, j, t, t, 0, person[1] - t, elephant[1] - t, mask | 1 << i | 1 << j), graph, dp)
    #             ans = max(ans, cost)

    ans = min_time(('AA', 'AA', 0, 0, mask), graph, dp, map_to_idx)
    return ans


inp = get_input()
start = time.time()
# print('Part 1:', part1(inp))
print('Part 2:', part2(inp))
print(time.time() - start)
