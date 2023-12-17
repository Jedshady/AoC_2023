#!/usr/bin/env python3 -u

import sys


def calculate_unmatch(left: str, right: str) -> int:
    return sum(l != r for l,r in zip(left, right))


def transpose_grid(grid: list()) -> list():
    return [''.join(row) for row in zip(*grid)]


def reflect_horizontal(grid: list[str], num_of_unmatch: int) -> int:
    for i in range(len(grid)):
        if i == 0:
            continue
        
        up = list(reversed(grid[:i]))
        down = grid[i:]

        # print(f"{i}: {up} and {down}")

        total_unmatch = 0
        for j in range(min(len(up), len(down))):
            total_unmatch += calculate_unmatch(up[j], down[j])
            
        if total_unmatch != num_of_unmatch:
            continue
        else:
            return i
        
    return 0


def part_1_or_2(grids: list(), num_of_unmatch: int = 0) -> int:
    total_num = 0
    for grid in grids:
        row = reflect_horizontal(grid, num_of_unmatch)
        col = reflect_horizontal(transpose_grid(grid), num_of_unmatch)

        # print(f"{row}, {col}")

        if row != 0:
            total_num += row * 100
        elif col != 0:
            total_num += col
    
    return total_num


def main():
    filename = sys.argv[1]

    grids = list()
    with open(filename, 'r') as file:
        grid = list()
        for line in file:
            if line.strip() != '':
                grid.append(line.strip())
            else:
                grids.append(grid)
                grid = list()
        grids.append(grid)

    # print(grids)

    part_1_res = part_1_or_2(grids, 0)
    part_2_res = part_1_or_2(grids, 1)

    print(f"{part_1_res}, {part_2_res}")



if __name__ == "__main__":
    main()