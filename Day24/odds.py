#!/usr/bin/env python3 -u

import sys
from z3 import *


def slope_intercept(p1, p2):
    if p2[0] - p1[0] == 0:  # Vertical line
        return float('inf'), p1[0]
    m = (p2[1] - p1[1]) / (p2[0] - p1[0])
    c = p1[1] - m * p1[0]
    return m, c


def line_intersection(seg1, seg2):
    (x1, y1), (x2, y2) = seg1
    (x3, y3), (x4, y4) = seg2

    m1, c1 = slope_intercept((x1, y1), (x2, y2))
    m2, c2 = slope_intercept((x3, y3), (x4, y4))

    # Parallel
    if m1 == m2:
        return (None, None)
    
    if m1 == float('inf'):
        x = c1
        y = m2 * x + c2
    elif m2 == float('inf'):
        x = c2
        y = m1 * x + c1
    else:
        x = (c2 - c1) / (m1 - m2)
        y = m1 * x + c1

    return (x, y)


def dot_product(vec1, vec2):
    return vec1[0] * vec2[0] + vec1[1] * vec2[1]


def part_1(hails: list(), test_range: tuple()) -> int:
    count = 0
    for i in range(len(hails)-1):
        for j in range(i+1, len(hails)):
            (h_i_x_s, h_i_y_s), (v_i_x, v_i_y) = hails[i][:2], hails[i][3:-1]
            (h_j_x_s, h_j_y_s), (v_j_x, v_j_y) = hails[j][:2], hails[j][3:-1]
            
            h_i_x_e, h_i_y_e = h_i_x_s + v_i_x, h_i_y_s + v_i_y
            h_j_x_e, h_j_y_e = h_j_x_s + v_j_x, h_j_y_s + v_j_y

            
            # print(f"{h_i_x_s=} {h_i_y_s=} {h_i_x_e=} {h_i_y_e=} {v_i_x=} {v_i_y=}")
            # print(f"{h_j_x_s=} {h_j_y_s=} {h_j_x_e=} {h_j_y_e=} {v_j_x=} {v_j_y=}\n")

            segment_i = ((h_i_x_s, h_i_y_s), (h_i_x_e, h_i_y_e))
            segment_j = ((h_j_x_s, h_j_y_s), (h_j_x_e, h_j_y_e))

            intersect_pt_x, intersect_pt_y = line_intersection(segment_i, segment_j)

            if intersect_pt_x and intersect_pt_y:
                if test_range[0] <= intersect_pt_x <= test_range[1] and test_range[0] <= intersect_pt_y <= test_range[1]:
                    vector_i = (intersect_pt_x - h_i_x_s, intersect_pt_y - h_i_y_s)
                    vector_j = (intersect_pt_x - h_j_x_s, intersect_pt_y - h_j_y_s)

                    dot_product_i = dot_product(vector_i, (v_i_x, v_i_y))
                    dot_product_j = dot_product(vector_j, (v_j_x, v_j_y))

                    intersect_in_future_i = dot_product_i > 0
                    intersect_in_future_j = dot_product_j > 0

                    if intersect_in_future_i and intersect_in_future_j:
                        count += 1

    return count   


def part_2(hails: list()):
    def f(s):
        return Real(s)
    
    x, y, z, vx, vy, vz = f('x'), f('y'), f('z'), f('vx'), f('vy'), f('vz')

    # T = [T0, T1, T2 ... ]
    T = [f(f"T{i}") for i in range(len(hails))]

    solve = Solver()

    # To solve this, only need three data points. so range(len(hails)-297) also works
    for i in range(len(hails)):
    # for i in range(len(hails)-297):
        solve.add(x + T[i] * vx - hails[i][0] - T[i] * hails[i][3] == 0)
        solve.add(y + T[i] * vy - hails[i][1] - T[i] * hails[i][4] == 0)
        solve.add(z + T[i] * vz - hails[i][2] - T[i] * hails[i][5] == 0)

    # print(f"{solve}")
        
    res = solve.check()
    M = solve.model()
    # print(f"{res=} {M.eval(x)=} {M.eval(y)=} {M.eval(z)=} {M.eval(vx)=} {M.eval(vy)=} {M.eval(vz)=}")

    return M.eval(x + y + z)



def main():
    filename = sys.argv[1]

    hails = list()

    with open(filename, 'r') as file:
        for line in file:
            l_x, l_y, l_z = map(int, line.strip().split(' @ ')[0].split(', '))
            v_x, v_y, v_z = map(int, line.strip().split(' @ ')[1].split(', '))
            hails.append([l_x, l_y, l_z, v_x, v_y, v_z])

    # print(f"{hails=}")
    
    if filename.split('/')[-1] == 'test_input':
        test_range = (7, 27)
    elif filename.split('/')[-1] == 'original_input':
        test_range = (200000000000000, 400000000000000)

    part_1_res = part_1(hails, test_range)
    part_2_res = part_2(hails)
    
    print(f"{part_1_res}, {part_2_res}")

if __name__ == "__main__":
    main()