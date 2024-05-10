#!/usr/bin/env python3 -u

import sys
import copy

def part_1(galaxies: list, x_without_galaxy: list, y_without_galaxy: list):
    for galaxy in galaxies:
        count_x = 0
        count_y = 0
        for i in x_without_galaxy:
            if i < galaxy[0]:
                count_x += 1

        for j in y_without_galaxy:
            if j < galaxy[1]:
                count_y += 1

        # print(f"Old loc: {galaxy}")        
        galaxy[0] += count_x
        galaxy[1] += count_y
        # print(f"New loc: {galaxy}")
        # print("******************")

    res = 0

    for i in range(len(galaxies)-1):
        for j in range(i+1, len(galaxies), 1):
            x_distance = abs(galaxies[j][0] - galaxies[i][0])
            y_distance = abs(galaxies[j][1] - galaxies[i][1])
            distance = x_distance + y_distance
            res += distance
            # print(f"Distance of galaxy {galaxies[i]} and {galaxies[j]} is {distance}")

    print(f"Part 1 result is {res}")


def part_2(galaxies: list, x_without_galaxy: list, y_without_galaxy: list, n: int = 1000000):
    for galaxy in galaxies:
        count_x = 0
        count_y = 0
        for i in x_without_galaxy:
            if i < galaxy[0]:
                count_x += n - 1

        for j in y_without_galaxy:
            if j < galaxy[1]:
                count_y += n - 1

        # print(f"Old loc: {galaxy}")        
        galaxy[0] += count_x
        galaxy[1] += count_y
        # print(f"New loc: {galaxy}")
        # print("******************")

    res = 0

    for i in range(len(galaxies)-1):
        for j in range(i+1, len(galaxies), 1):
            x_distance = abs(galaxies[j][0] - galaxies[i][0])
            y_distance = abs(galaxies[j][1] - galaxies[i][1])
            distance = x_distance + y_distance
            res += distance
            # print(f"Distance of galaxy {galaxies[i]} and {galaxies[j]} is {distance}")

    print(f"Part 2 result is {res}")



def main():
    filename = sys.argv[1]

    grid = list()
    
    with open(filename, 'r') as file:
        for line in file:
            grid.append(line)

    # print(grid)

    galaxies = list()
    x_with_galaxy = set() 
    y_with_galaxy = set()

    for x, line in enumerate(grid):
        for y, point in enumerate(line):
            if point == '#':
                galaxies.append([x, y])
                x_with_galaxy.add(x)
                y_with_galaxy.add(y)

    # print(galaxy_loc)
    # print(sortedlist(x_with_galaxy)))
    # print(sorted(list(y_with_galaxy)))
                
    x_without_galaxy = []
    y_without_galaxy = []

    for i in range(len(grid)):
        if i not in x_with_galaxy:
            x_without_galaxy.append(i)
    
    for j in range(len(grid[0])):
        if j not in y_with_galaxy:
            y_without_galaxy.append(j)

    
    part_1_galaxies = copy.deepcopy(galaxies)

    # Part 1
    part_1(part_1_galaxies, x_without_galaxy, y_without_galaxy)


    # Part 2
    if len(sys.argv) == 3:        
        n = sys.argv[2]
        part_2(galaxies, x_without_galaxy, y_without_galaxy, int(n))
    else:
        part_2(galaxies, x_without_galaxy, y_without_galaxy)


if __name__ == "__main__":
    main()