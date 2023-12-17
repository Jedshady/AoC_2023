#!/usr/bin/env python3 -u

import sys
import re

def calculate_hash(s: str) -> int:
    cur_hash = 0
    for c in s:
        cur_hash += ord(c)
        cur_hash *= 17
        cur_hash %= 256
        # print(f"After {c}, hash is {cur_hash}.")
    return cur_hash


def part_1(notes: list()) -> int:
    total_hash = 0

    for note in notes:
        total_hash += calculate_hash(note)
        # print(f"After {note}, total hash is {total_hash}")
    
    return  total_hash


def part_2(notes: list()) -> int:
    boxes = [{'num_of_lens': 0} for _ in range(256)]

    for note in notes:
        new_note = re.split('[=-]', note)[0]

        box_num = calculate_hash(new_note)
        # print(f"{new_note} cooresponds box {box_num}")

        cur_box = boxes[box_num]

        if note[len(new_note)] == '=':
            focal_length = int(re.split('=', note)[1])
            if new_note not in cur_box:
                cur_box[new_note] = [cur_box['num_of_lens']+1, focal_length]
                cur_box['num_of_lens'] += 1
                # print(f"After adding a new lense, box {box_num} is like {cur_box}")
            else:
                cur_box[new_note][1] = focal_length
                # print(f"Replaced a lense, box {box_num} is like {cur_box}")

        if note[len(new_note)] == '-':
            if new_note not in cur_box:
                continue
            else:
                pos, _ = cur_box.pop(new_note)
                cur_box['num_of_lens'] -= 1
                for key, value in cur_box.items():
                    # print(f"{key}, {value}")
                    if key != 'num_of_lens':
                        if value[0] > pos:
                            value[0] -= 1


    focusing_power = 0
    for box in boxes:
        idx_box = boxes.index(box)
        if box['num_of_lens'] != 0:
            for key, value in box.items():
                if key != 'num_of_lens':
                    focusing_power += (idx_box + 1) * value[0] * value[1]

    # print(focusing_power)

    return focusing_power



def main():
    filename = sys.argv[1]

    notes = list()
    with open(filename, 'r') as file:
        for line in file:
            notes = line.strip().split(',')

    # print(note)

    part_1_res = part_1(notes)
    part_2_res = part_2(notes)
    print(f"{part_1_res}, {part_2_res}")

             
    
if __name__ == "__main__":

    main()