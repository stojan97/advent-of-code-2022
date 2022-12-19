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
    # go through each node with flow
    idx = 0
    # shortest_path_to_other_for_valve('AA', graph)

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
    return final_graph


def find_max_remaining_cost(current, graph):
    idx, time, time_spent, pressure, bitmask, path = current

    # open valve
    if path != '':
        path += '->'
    path += graph[idx][0]

    flow = time_spent * pressure
    pressure += graph[idx][2]

    ans = flow + (30 - time) * pressure

    # visit adj
    for i, t in graph[idx][3]:
        next_time = time + t
        if not (bitmask & (1 << i)) and next_time <= 30:
            ans = max(ans, flow + find_max_remaining_cost((i, next_time, t, pressure, bitmask | 1 << i, path), graph))

    return ans


def part1(graph):
    mask = 1 << len(graph)
    ans = 0
    for idx, node in enumerate(graph):
        ans = max(ans, find_max_remaining_cost((idx, node[1], node[1], 0, mask | 1 << idx, ''), graph))

    return ans


def find_max_cost(current, graph):
    p_idx, e_idx, time, flow, pressure, rem_p, rem_e, bitmask_covered, bitmask_opened, path1, path2 = current

    p_idx, e_idx, time, flow, pressure, rem_p, rem_e, bitmask_rem, path1, path2 = q.popleft()
    id += 1

    if time > 26:
        continue

    if p_idx is not None:
        if path1 != '':
            path1 += '->'
        path1 += graph[p_idx][0]

    if e_idx is not None:
        if path2 != '':
            path2 += '->'
        path2 += graph[e_idx][0]

    person_opens = p_idx is not None and rem_p == 0
    elephant_opens = e_idx is not None and rem_e == 0

    if person_opens:
        pressure += graph[p_idx][2]

    #
    # if p_idx == 5 and e_idx == 2:
    #     print(
    #         f'{id}: AFTER OPEN VALVE: == Minute {time} == person_path={path1}, elephant_path={path2}, flow={flow}, until_26_flow={flow + (26 - time) * pressure}, pressure={pressure}, bitmask_rem={bitmask_rem}')

    if elephant_opens:
        pressure += graph[e_idx][2]

    # print(
    #     f'{id}: == Minute {time} == person_path={path1}, elephant_path={path2}, remaining_person={rem_p}, remaining_elephant={rem_e} flow={flow}, until_26_flow={flow + (26 - time) * pressure}, pressure={pressure}, bitmask_rem={bitmask_rem}')

    # dp(time, last_node, remaining_bitmask) = memo

    total_pressure = flow + (26 - time) * pressure

    if id % 1_000_000 == 0:
        print(
            f'{id}: == Minute {time} :: person_path={path1}, elephant_path={path2}, remaining_time_person={rem_p}, remaining_time_elephant={rem_e} flow={flow}, until_26_flow={flow + (26 - time) * pressure}, pressure={pressure}, bitmask_rem={bitmask_rem}')
        print(ans)

    ans = max(ans, total_pressure)

    if path1.startswith('JJ') and path2.startswith('DD->HH->HH->EE'):
        print(
            f'== Minute {time} :: person_path={path1}, elephant_path={path2}, remaining_time_person={rem_p}, remaining_time_elephant={rem_e} flow={flow}, until_26_flow={flow + (26 - time) * pressure}, pressure={pressure}, bitmask_rem={bitmask_rem}')

    none_replacement = [(None, math.inf)]

    if rem_p > 0:
        person_next = [(p_idx, rem_p)]
    else:
        person_next = [(i, t) for i, t in graph[p_idx][3] if
                       not (bitmask_rem & (1 << i))] if p_idx is not None else []

    if rem_e > 0:
        elephant_next = [(e_idx, rem_e)]
    else:
        elephant_next = [(i, t) for i, t in graph[e_idx][3] if
                         not (bitmask_rem & (1 << i))] if e_idx is not None else []

    if not person_next and not elephant_next:
        continue

    if not person_next:
        person_next = none_replacement

    if not elephant_next:
        elephant_next = none_replacement

    # if path1.startswith('JJ->JJ->BB->CC') and path2.startswith('DD->HH->HH->EE'):
    #     print(person_next, elephant_next)

    for (i, t1), (j, t2) in product(person_next, elephant_next):
        t = min(t1, t2)
        next_time = time + t
        if i != j and next_time <= 26:
            mask_i = (1 << i) if i is not None else 0
            mask_j = (1 << j) if j is not None else 0

            next = (i, j, next_time, t, pressure, t1 - t, t2 - t, bitmask_rem | mask_i | mask_j, path1, path2)


    # f(current) = flow + f(adj, t + 1)
    # f(last_node, bitmask, t) = last_node with next set bitmask, at time t
    return ans


def part2(graph):
    mask = 1 << len(graph)
    full_mask = (1 << (len(graph) + 1)) - 1
    print(mask, full_mask)
    ans = 0
    print('Graph', graph)

    for i, person in enumerate(graph):
        # for elephant
        for j, elephant in enumerate(graph):
            if i != j:
                # p_idx, e_idx, time, flow, pressure, rem_p, rem_e, bitmask_rem, valve_p, valve_e, path1, path2
                t = min(person[1], elephant[1])
                cost = find_max_cost(
                    (i, j, t, 0, 0, person[1] - t, elephant[1] - t, mask | 1 << i | 1 << j, mask, '', ''))
                ans = max(ans, cost)
    #
    # while q:
    #     p_idx, e_idx, time, flow, pressure, rem_p, rem_e, bitmask_rem, path1, path2 = q.popleft()
    #     id += 1
    #
    #     if time > 26:
    #         continue
    #
    #     if p_idx is not None:
    #         if path1 != '':
    #             path1 += '->'
    #         path1 += graph[p_idx][0]
    #
    #     if e_idx is not None:
    #         if path2 != '':
    #             path2 += '->'
    #         path2 += graph[e_idx][0]
    #
    #     person_opens = p_idx is not None and rem_p == 0
    #     elephant_opens = e_idx is not None and rem_e == 0
    #
    #     if person_opens:
    #         pressure += graph[p_idx][2]
    #
    #     #
    #     # if p_idx == 5 and e_idx == 2:
    #     #     print(
    #     #         f'{id}: AFTER OPEN VALVE: == Minute {time} == person_path={path1}, elephant_path={path2}, flow={flow}, until_26_flow={flow + (26 - time) * pressure}, pressure={pressure}, bitmask_rem={bitmask_rem}')
    #
    #     if elephant_opens:
    #         pressure += graph[e_idx][2]
    #
    #     # print(
    #     #     f'{id}: == Minute {time} == person_path={path1}, elephant_path={path2}, remaining_person={rem_p}, remaining_elephant={rem_e} flow={flow}, until_26_flow={flow + (26 - time) * pressure}, pressure={pressure}, bitmask_rem={bitmask_rem}')
    #
    #     # dp(time, last_node, remaining_bitmask) = memo
    #
    #     total_pressure = flow + (26 - time) * pressure
    #
    #     if id % 1_000_000 == 0:
    #         print(
    #             f'{id}: == Minute {time} :: person_path={path1}, elephant_path={path2}, remaining_time_person={rem_p}, remaining_time_elephant={rem_e} flow={flow}, until_26_flow={flow + (26 - time) * pressure}, pressure={pressure}, bitmask_rem={bitmask_rem}')
    #         print(ans)
    #
    #     ans = max(ans, total_pressure)
    #
    #     if path1.startswith('JJ') and path2.startswith('DD->HH->HH->EE'):
    #         print(
    #             f'== Minute {time} :: person_path={path1}, elephant_path={path2}, remaining_time_person={rem_p}, remaining_time_elephant={rem_e} flow={flow}, until_26_flow={flow + (26 - time) * pressure}, pressure={pressure}, bitmask_rem={bitmask_rem}')
    #
    #     none_replacement = [(None, math.inf)]
    #
    #     if rem_p > 0:
    #         person_next = [(p_idx, rem_p)]
    #     else:
    #         person_next = [(i, t) for i, t in graph[p_idx][3] if
    #                        not (bitmask_rem & (1 << i))] if p_idx is not None else []
    #
    #     if rem_e > 0:
    #         elephant_next = [(e_idx, rem_e)]
    #     else:
    #         elephant_next = [(i, t) for i, t in graph[e_idx][3] if
    #                          not (bitmask_rem & (1 << i))] if e_idx is not None else []
    #
    #     if not person_next and not elephant_next:
    #         continue
    #
    #     if not person_next:
    #         person_next = none_replacement
    #
    #     if not elephant_next:
    #         elephant_next = none_replacement
    #
    #     # if path1.startswith('JJ->JJ->BB->CC') and path2.startswith('DD->HH->HH->EE'):
    #     #     print(person_next, elephant_next)
    #
    #     for (i, t1), (j, t2) in product(person_next, elephant_next):
    #         t = min(t1, t2)
    #         next_time = time + t
    #         if i != j and next_time <= 26:
    #             mask_i = (1 << i) if i is not None else 0
    #             mask_j = (1 << j) if j is not None else 0
    #
    #             next = (i, j, next_time, flow + pressure * t, pressure, t1 - t, t2 - t, bitmask_rem | mask_i | mask_j,
    #                     path1, path2)
    #             # if path1.startswith('JJ->JJ->BB->CC') and path2.startswith('DD->HH->HH->EE'):
    #             #     print('Next:', next)
    #             q.append(next)

    return ans


inp = get_input()
start = time.time()
# print('Part 1:', part1(inp))
print('Part 2:', part2(inp))
print(time.time() - start)
