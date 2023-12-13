#!/usr/bin/env python3 -u

import sys
from datetime import datetime

def main():
    filename = sys.argv[1]
    
    grid: list(str) = list()
    
    start_point = [None, None]
    
    with open(filename, 'r') as file:
        for line in file:
            S_idx = line.find('S')
            if S_idx != -1:
                start_point[0] = len(grid)
                start_point[1] = S_idx
            
            grid.append(line)
    
    # print(grid)
    # print(start_point)

    trace = list()
    points = [start_point]
    cur_point = start_point

    found_path = False

    if not found_path and cur_point[0] - 1 >= 0:
        # print("Checking above")
        x = cur_point[0] - 1
        y = cur_point[1]
        if grid[x][y] in ('|', '7', 'F'):
            cur_point = [x, y]
            found_path = True
            trace.append('U')
    
    if not found_path and cur_point[1] + 1 <= len(grid[0]):
        # print("Checking right")
        x = cur_point[0]
        y = cur_point[1] + 1
        if grid[x][y] in ('-', 'J', '7'):
            cur_point = [x, y]
            found_path = True
            trace.append('R')
    
    if not found_path and cur_point[0] + 1 <= len(grid):
        # print("Checking bottom")
        x = cur_point[0] + 1
        y = cur_point[1]
        if grid[x][y] in ('|', 'J', 'L'):
            cur_point = [x, y]
            found_path = True
            trace.append('D')
    
    if not found_path and cur_point[1] - 1 >= 0:
        # print("Checking left")
        x = cur_point[0]
        y = cur_point[1] - 1
        if grid[x][y] in ('-', 'L', 'F'):
            cur_point = [x, y]
            found_path = True
            trace.append('L')
       
    # print(cur_point)

    while grid[cur_point[0]][cur_point[1]] != 'S':
        points.append(cur_point)
        nav = grid[cur_point[0]][cur_point[1]]
        # print(f"nav is {nav}")
        last_move = trace[-1]
        if nav == '|':
            if last_move == 'U':
                cur_point = [cur_point[0]-1, cur_point[1]]
                trace.append('U')
            if last_move == 'D':
                cur_point = [cur_point[0]+1, cur_point[1]]
                trace.append('D')
        if nav == '7':
            if last_move == 'U':
                cur_point = [cur_point[0], cur_point[1]-1]
                trace.append('L')
            if last_move == 'R':
                cur_point = [cur_point[0]+1, cur_point[1]]
                trace.append('D')
        if nav == 'F':
            if last_move == 'U':
                cur_point = [cur_point[0], cur_point[1]+1]
                trace.append('R')
            if last_move == 'L':
                cur_point = [cur_point[0]+1, cur_point[1]]
                trace.append('D')
        if nav == '-':
            if last_move == 'R':
                cur_point = [cur_point[0], cur_point[1]+1]
                trace.append('R')
            if last_move == 'L':
                cur_point = [cur_point[0], cur_point[1]-1]
                trace.append('L')
        if nav == 'J':
            if last_move == 'D':
                cur_point = [cur_point[0], cur_point[1]-1]
                trace.append('L')
            if last_move == 'R':
                cur_point = [cur_point[0]-1, cur_point[1]]
                trace.append('U')
        if nav == 'L':
            if last_move == 'D':
                cur_point = [cur_point[0], cur_point[1]+1]
                trace.append('R')
            if last_move == 'L':
                cur_point = [cur_point[0]-1, cur_point[1]]
                trace.append('U')


    # print(trace)
    # print(points)

    # Part 1
    mid_way = int(len(trace) / 2)
    print(f"Part 1: mid way is {mid_way}")

    # Part 2
    # Shoelace formula: https://en.wikipedia.org/wiki/Shoelace_formula
    # Need to take absolute value because calculations clock-wise and anti-clock-wise is opposite to each other
    padded_points = [*points, points[0]]  # append the start point
    area = abs(sum(
            row1 * col2 - row2 * col1
            for (row1, col1), (row2, col2) in zip(padded_points, padded_points[1:])
        ) / 2)

    # print(padded_points)
    # print(abs(area))

    # Pick's theorem: https://en.wikipedia.org/wiki/Pick%27s_theorem
    num_interior_points = int(abs(area) - 0.5 * len(points) + 1)
    print(f"Part 2: number of interior point is {num_interior_points}")


if __name__ == "__main__":
    # start = datetime.now()
    main()
    # end = datetime.now()
    # elapsed = (end - start).microseconds / 1000 
    # print(f"Whole process took {elapsed}ms")