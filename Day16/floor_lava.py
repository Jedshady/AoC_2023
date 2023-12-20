#!/usr/bin/env python3 -u

import sys
from math import inf

'''
    -1 Mirror
    (0,  1) left to right
    (0, -1) right to left
    (1,  0) top to bottom
    (-1, 0) bottom to top
'''

def visit_point(last_point: tuple(), cur_point: tuple(), 
                last_visited: list(), to_visit: list(), 
                energized: dict(), grid: list()) -> None:
    last_x = last_point[0]
    last_y = last_point[1]
    cur_x = cur_point[0]
    cur_y = cur_point[1]

    # print(f"Last point: {last_point}")
    # print(f"Current point: {cur_point}")

    if cur_x < 0 or cur_x >= len(grid) or cur_y < 0 or cur_y >= len(grid[0]):
        # print("Out of the boundary. Light ends.")
        return
    
    # print(f"Current char is {grid[cur_x][cur_y]}")
    
    if grid[cur_x][cur_y] == '|':
        if last_y == cur_y:
            # vertical through
            if last_x < cur_x:
                # light comes from up
                energized[cur_point] = -1
                last_visited.append(cur_point)
                to_visit.append((cur_x+1, cur_y))
            elif last_x > cur_x:
                # light comes from bottom
                energized[cur_point] = -1
                last_visited.append(cur_point)
                to_visit.append((cur_x-1, cur_y))
        elif last_x == cur_x:
            # vertical two way
            energized[cur_point] = -1
            last_visited.append(cur_point)
            last_visited.append(cur_point)
            to_visit.append((cur_x-1, cur_y))
            to_visit.append((cur_x+1, cur_y))
    
    if grid[cur_x][cur_y] == '-':
        if last_x == cur_x:
            # horizontal through
            if last_y < cur_y:
                # light comes from left
                energized[cur_point] = -1
                last_visited.append(cur_point)
                to_visit.append((cur_x, cur_y+1))
            elif last_y > cur_y:
                # light comes from right
                energized[cur_point] = -1
                last_visited.append(cur_point)
                to_visit.append((cur_x, cur_y-1))
        elif last_y == cur_y:
            # vertical two way
            energized[cur_point] = -1
            last_visited.append(cur_point)
            last_visited.append(cur_point)
            to_visit.append((cur_x, cur_y-1))
            to_visit.append((cur_x, cur_y+1))

    if grid[cur_x][cur_y] == '\\':
        if last_x < cur_x or last_y < cur_y:
            # offset from last point is (1, 1)
            energized[cur_point] = -1
            last_visited.append(cur_point)
            to_visit.append((last_x+1, last_y+1))
        elif last_x > cur_x or last_y > cur_y:
            # offset from last point is (-1, -1)
            energized[cur_point] = -1
            last_visited.append(cur_point)
            to_visit.append((last_x-1, last_y-1))

    if grid[cur_x][cur_y] == '/':
        if last_x > cur_x or last_y < cur_y:
            # offset from last point is (-1, 1)
            energized[cur_point] = -1
            last_visited.append(cur_point)
            to_visit.append((last_x-1, last_y+1))
        elif last_x < cur_x or last_y > cur_y:
            # offset from last point is (1, -1)
            energized[cur_point] = -1
            last_visited.append(cur_point)
            to_visit.append((last_x+1, last_y-1))

    if grid[cur_x][cur_y] == '.':
        offset = (cur_x - last_x, cur_y - last_y)
        next_point = tuple(a + b for a, b in zip(cur_point, offset))
        if cur_point not in energized:
            energized[cur_point] = [offset]
        else:
            if offset in energized[cur_point]:
                # print("Have hit this point from the same direction.")
                return
            else:
                energized[cur_point].append(offset)   

        last_visited.append(cur_point)
        to_visit.append(next_point)


def part_1(grid: list()) -> int:
    energized = dict()
    last_visited = [(0,-1)]

    to_visit = [(0, 0)]

    while to_visit:
        last_point = last_visited.pop()
        cur_point = to_visit.pop()
        visit_point(last_point, cur_point, last_visited, to_visit, energized, grid)

    return len(energized)


def part_2(grid: list()) -> int:

    max_energy = -inf

    # top down
    for i in range(len(grid[0])):
        energized = dict()
        last_visited = [(-1, i)]
        to_visit = [(0, i)]

        while to_visit:
            last_point = last_visited.pop()
            cur_point = to_visit.pop()
            visit_point(last_point, cur_point, last_visited, to_visit, energized, grid)
        
        # print(f"Max from top down: {len(energized)}")
        if len(energized) > max_energy:
            max_energy = len(energized)
    

    # bottom up
    for i in range(len(grid[0])):
        energized = dict()
        last_visited = [(len(grid), i)]
        to_visit = [(len(grid)-1, i)]

        while to_visit:
            last_point = last_visited.pop()
            cur_point = to_visit.pop()
            visit_point(last_point, cur_point, last_visited, to_visit, energized, grid)

        # print(f"Max from bottom up: {len(energized)}")
        if len(energized) > max_energy:
            max_energy = len(energized)

    # left to right
    for i in range(len(grid)):
        energized = dict()
        last_visited = [(i, -1)]
        to_visit = [(i, 0)]

        while to_visit:
            last_point = last_visited.pop()
            cur_point = to_visit.pop()
            visit_point(last_point, cur_point, last_visited, to_visit, energized, grid)

        # print(f"Max from left to right: {len(energized)}")
        if len(energized) > max_energy:
            max_energy = len(energized)

    # right to left
    for i in range(len(grid)):
        energized = dict()
        last_visited = [(i, len(grid[0]))]
        to_visit = [(i, len(grid[0])-1)]

        while to_visit:
            last_point = last_visited.pop()
            cur_point = to_visit.pop()
            visit_point(last_point, cur_point, last_visited, to_visit, energized, grid)

        # print(f"Max from right to left: {len(energized)}")
        if len(energized) > max_energy:
            max_energy = len(energized)

    return max_energy




def main():
    filename = sys.argv[1]

    grid = list()

    with open(filename, 'r') as file:
        for line in file:
            grid.append(line.strip())

    # print(grid)
    
    part_1_res = part_1(grid)
    part_2_res = part_2(grid)
    print(f"{part_1_res}, {part_2_res}")



if __name__ == "__main__":
    main()