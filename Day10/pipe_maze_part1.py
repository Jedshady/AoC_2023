#!/usr/bin/env python3 -u


def main():
    filename = "original_input"
    
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

    mid_way = 0
    trace = list()
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
    mid_way = int(len(trace) / 2)
    print(f"mid way is {mid_way}")
            

if __name__ == "__main__":
    main()