#!/usr/bin/env python3 -u

import sys

OFFSETS = {'R': (0, 1), 'D': (1, 0), 'L': (0, -1), 'U': (-1, 0)}
DIRECTIONS = ['R', 'D', 'L', 'U']

# Shoelace formula: https://en.wikipedia.org/wiki/Shoelace_formula
def calculate_area(points: list()) -> float:
    return abs(sum(
        row1 * col2 - row2 * col1
        for (row1, col1), (row2, col2) in zip(points, points[1:])
    ) / 2)


# Pick's theorem: https://en.wikipedia.org/wiki/Pick%27s_theorem
def interior_points(area: float, boundary: list()) -> int:
    return int(abs(area) - 0.5 * sum(boundary) + 1)


def part_1(inputs):
    points = [(0, 0)]
    boundary = []

    for input in inputs:
        for k, v in OFFSETS.items():
            if input[0] == k:
                new_x = points[-1][0] + v[0] * input[1]
                new_y = points[-1][1] + v[1] * input[1]
                points.append((new_x, new_y))
                boundary.append(input[1])
    
    area = calculate_area(points)
    num_interior_points = interior_points(area, boundary)

    return sum(boundary) + num_interior_points
 

def part_2(inputs):
    new_inputs = []
    for input in inputs:
        direction = DIRECTIONS[int(input[2][-1])]
        steps = int(input[2][1:-1], 16)
        new_inputs.append([direction, steps])

    # print(new_inputs)

    return part_1(new_inputs)


def main():
    filename = sys.argv[1]
    
    inputs = []

    with open(filename, 'r') as file:
        for line in file:
            direction, steps, color = line.split(' ')
            inputs.append([direction, int(steps), color.strip().strip('[(|)]')])

    # print(inputs)

    part_1_res = part_1(inputs)

    part_2_res = part_2(inputs)
    
    print(f"{part_1_res}, {part_2_res}")



if __name__ == "__main__":
    main()