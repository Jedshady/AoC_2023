#!/usr/bin/env python3 -u

import sys


def transpose_grid(grid: list()) -> list():
    return [''.join(row) for row in zip(*grid)]


def tilt_left(grid: list()) -> list():
    tilted_grid = list()
    length = len(grid[0])
    
    for line in grid:
        cur_load = length
        tilted_line = [None for _ in range(length)]
        for i in range(length):
            if line[i] == 'O':
                if cur_load + i != length:
                    tilted_line[i] = 'O'
                    tilted_line[length - cur_load], tilted_line[i] = tilted_line[i], tilted_line[length - cur_load]
                else:
                    tilted_line[i] = 'O'
                cur_load -= 1
            elif line[i] == '#':
                tilted_line[i] = '#'
                cur_load = length - i - 1
            else:
                tilted_line[i] = '.'
                continue
            
            # print(tilted_line)

        tilted_grid.append(''.join(tilted_line))

    # print(tilted_grid)

    return tilted_grid


def tilt_right(grid: list()) -> list():
    tilted_grid = list()
    length = len(grid[0])
    
    for line in grid:
        cur_load = 1
        tilted_line = [None for _ in range(length)]
        for i in range(length-1, -1, -1):
            if line[i] == 'O':
                if cur_load + i != length:
                    tilted_line[i] = 'O'
                    tilted_line[length - cur_load], tilted_line[i] = tilted_line[i], tilted_line[length - cur_load]
                else:
                    tilted_line[i] = 'O'
                cur_load += 1
            elif line[i] == '#':
                tilted_line[i] = '#'
                cur_load = length + 1 - i
            else:
                tilted_line[i] = '.'
                continue
            
            # print(tilted_line)

        tilted_grid.append(''.join(tilted_line))

    # print(tilted_grid)

    return tilted_grid


def calculate_north_load(grid: list()) -> int:
    total_load = 0
    for i in range(len(grid)):
        total_load += (len(grid) - i) * grid[i].count('O')
    
    return total_load


def part_1(original_grid: list()):
    tilted_north = transpose_grid(tilt_left(transpose_grid(original_grid)))
    return calculate_north_load(tilted_north)


def part_2(original_grid: list(), num_of_cycle: int = 1000000000):

    # print(f"After cycle 0: {original_grid}")

    grid2cycle = dict()

    cur_grid = original_grid
    grid2cycle['|'.join(cur_grid)] = 0
    found_cycle = -1
    for i in range(1, num_of_cycle + 1):
        tilted_north = transpose_grid(tilt_left(transpose_grid(cur_grid)))
        tilted_west = tilt_left(tilted_north)
        tilted_south = transpose_grid(tilt_right(transpose_grid(tilted_west)))
        tilted_east = tilt_right(tilted_south)

        # print(f"After cycle {i}, {tilted_east}") 
        cur_grid = tilted_east
        
        cur_key = '|'.join(cur_grid)
        if cur_key in grid2cycle:
            found_cycle = grid2cycle[cur_key]
            break
        else:
            grid2cycle[cur_key] = i

    # print(f"Running for { num_of_cycle } cycles.")
    # print(f"The start of a cycle is cycle {found_cycle}.")
    # print(f"The end of a cycle is cycle {i}.")
    
    remainder = (num_of_cycle - found_cycle) % (i - found_cycle)
    # print(f"Reminder = {remainder} so the last grid looks like cycle {found_cycle + remainder}.")

    for key, value in grid2cycle.items():
        if value == found_cycle + remainder:
            grid = key.split('|')
            # print(grid)
            return calculate_north_load(grid)

    print(f"Did not find.")
    return 0


def main():
    filename = sys.argv[1]

    original_grid = list()

    with open(filename, 'r') as file:
        for line in file:
            original_grid.append(line.strip())

    part_1_res = part_1(original_grid)

    if len(sys.argv) == 3:
        cycle = int(sys.argv[2])
        part_2_res = part_2(original_grid, cycle)
    else:
        part_2_res = part_2(original_grid)

    print(f"{part_1_res}, {part_2_res}")


if __name__ == "__main__":
    main()