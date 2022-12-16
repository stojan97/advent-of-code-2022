import re
import time


def dist(p1, p2):
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])


def get_input():
    lines = []
    sensors = []
    beacons = set()

    with open('input') as file:
        for line in file:
            points = re.findall(r'[+-]?\d+', line.strip())
            lines.append(points)
            sensor_pos = (int(points[1]), int(points[0]))
            beacon_pos = (int(points[3]), int(points[2]))
            coverage = dist(sensor_pos, beacon_pos)
            sensors.append((sensor_pos[0], sensor_pos[1], coverage))
            beacons.add(beacon_pos)

    return sensors, beacons


def get_merged_intervals(intervals):
    # print(intervals)
    intervals.sort()
    merged = []

    for interval in intervals:
        if not merged:
            merged.append(interval)
            continue

        if interval[0] <= merged[-1][1]:
            merged[-1] = (merged[-1][0], max(merged[-1][1], interval[1]))
        else:
            merged.append(interval)

    return merged


def get_interval_from_row(sensor, row):
    x, y, coverage = sensor

    intersecting_point = (row, y)
    distance = dist((x, y), intersecting_point)

    if distance > coverage:
        return None

    spread = coverage - distance

    return y - spread, y + spread


def prepare_intervals(sensors, row, adjust):
    intervals = []
    for sensor in sensors:
        interval = get_interval_from_row(sensor, row)
        if interval:
            intervals.append(adjust(interval))

    return intervals


def get_intervals(sensors, row, adjust):
    intervals = prepare_intervals(sensors, row, adjust)
    return get_merged_intervals(intervals)


def part1(input):
    sensors, beacons = input
    row = 2_000_000
    merged_intervals = get_intervals(sensors, row, lambda i: i)
    spread_intervals = sum(m_interval[1] - m_interval[0] + 1 for m_interval in merged_intervals)
    beacons_on_row = sum(int(beacon[0] == row) for beacon in beacons)

    return spread_intervals - beacons_on_row


def part2_alternative(input):
    sensors, beacons = input
    limit = 4_000_000
    tuning_freq_mul = 4_000_000

    for sensor in sensors:
        touching_point = sensor.get_point_if_touching(sensors, limit)
        if touching_point:
            print(sensor, touching_point)
            return touching_point[1] * tuning_freq_mul + touching_point[0]

    return -1


def part2(input):
    sensors, beacons = input
    limit = 4_000_000
    tuning_freq_mul = 4_000_000
    adjust = lambda i: (max(i[0], 0), min(i[1], limit))

    for row in range(limit + 1):
        intervals = get_intervals(sensors, row, adjust)
        if row % 100_000 == 0:
            print(f'Row: {row} ::: intervals={intervals}')

        if len(intervals) == 2 and intervals[0][1] + 2 == intervals[1][0]:
            return (intervals[0][1] + 1) * tuning_freq_mul + row

    return -1


inp = get_input()
print('Part 1:', part1(inp))
start = time.time()
# 50 secs
print('Part 2:', part2(inp))
print(time.time() - start)
