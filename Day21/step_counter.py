#!/usr/bin/env python3 -u

import sys
from functools import cache
import logging

logging.basicConfig(level=logging.INFO, filemode='w')

# (U, R, D, L)
OFFSETS = ((-1, 0), (0, 1), (1, 0), (0, -1))

@cache
def explore_point(cur_point: tuple(), grid: tuple()) -> tuple():
    next_step_points = list()
    for offset_x, offset_y in OFFSETS:
        explore_x = cur_point[0] + offset_x
        explore_y = cur_point[1] + offset_y
        if 0 <= explore_x < len(grid) and 0 <= explore_y < len(grid[0]):
            equivalent_x = explore_x
            equivalent_y = explore_y
        else:
            equivalent_x = explore_x % len(grid)
            equivalent_y = explore_y % len(grid[0])
            logging.debug(f"Exploring point {(explore_x, explore_y)} is outside of current grid.")
            logging.debug(f"Replaced with {(equivalent_x, equivalent_y)}")

        if grid[equivalent_x][equivalent_y] != '#':
            next_step_points.append((explore_x, explore_y))

    return tuple(next_step_points)


def part_1(start_point: tuple(), grid: tuple(), total_steps: int) -> int:
    cur_step = 1
    cur_step_points = [start_point]

    while cur_step <= total_steps:
        next_step_points = set()
        while cur_step_points:
            cur_point = cur_step_points.pop()
            logging.debug(f"{cur_step=} {cur_point=}")
            possible_points = explore_point(cur_point, grid)
            for point in possible_points:
                next_step_points.add(point)
        cur_step_points = list(next_step_points)
        cur_step += 1

    logging.debug(f"{cur_step_points}")

    return len(cur_step_points)


def main():
    filename = sys.argv[1]

    grid = list()
    start_point = tuple()

    with open(filename, 'r') as file:
        for line in file:
            if 'S' in line:
                start_point = (len(grid), line.find('S'))
            grid.append(line.strip())
                
    grid = tuple(grid)

    # logging.debug(f"{grid=}")
    # logging.debug(f"{start_point=}")

    part_1_res = part_1(start_point, grid, 50)
    print(f"{part_1_res}")



    

if __name__ == "__main__":
    main()