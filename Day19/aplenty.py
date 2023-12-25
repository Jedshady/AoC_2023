#!/usr/bin/env python3 -u

import sys
import re
import copy
import logging
from collections import deque

logging.basicConfig(level=logging.INFO, filemode='w')


def test_workflow(part: list(), flowname: str, workflows: dict()) -> [str, str]:
    for key, value in part.items():
        globals()[key] = value
        
    # logging.debug(f"{x=} {m=} {a=} {s=}")

    workflow = workflows[flowname]
    for flow in workflow:
        if ':' in flow:
            rule, potential_flow = flow.split(':')
            if eval(rule):
                next_flow = potential_flow
            else:
                continue
        else:
            next_flow = flow

        if next_flow in ['A', 'R']:
            return None, next_flow
        else:
            return next_flow, None


def part_1(workflows: dict(), parts: list(), parts_total: list()) -> int:
    final_state = []
                
    for part in parts:
        next_flow, state = test_workflow(part, 'in', workflows)
        logging.debug(f"{next_flow=} {state=}")
        while state not in ['A', 'R']:
            next_flow, state = test_workflow(part, next_flow, workflows)
            logging.debug(f"{next_flow=} {state=}")
 
        final_state.append(state)

    logging.debug(f"{final_state=}")

    return sum(value for state, value in zip(final_state, parts_total) if state == 'A')


def reduce_range(cur_range: dict(), rule: str) -> [dict(), dict()]:
    new_range = copy.deepcopy(cur_range)
    opp_range = copy.deepcopy(cur_range)

    ch = rule[0]

    cur_filter = eval("lambda " + rule[0] + ": " + rule)
    neg_cur_filter = eval("lambda " + rule[0] + ": not (" + rule + ")")

    filtered_list = list(filter(cur_filter, range(cur_range[ch][0], cur_range[ch][1]+1)))
    neg_filtered_list = list(filter(neg_cur_filter, range(cur_range[ch][0], cur_range[ch][1]+1)))

    if filtered_list and neg_filtered_list:
        new_range[ch] = [filtered_list[0], filtered_list[-1]]
        opp_range[ch] = [neg_filtered_list[0], neg_filtered_list[-1]]
    elif not filtered_list:
        new_range = None
    elif not neg_cur_filter:
        opp_range = None

    return new_range, opp_range 


def part_2(workflows: dict()) -> int:
    initial_parts_range = {'x': [1, 4000], 'm': [1, 4000], 'a': [1, 4000], 's': [1, 4000]}

    reduce_list = deque([['in', initial_parts_range]])

    acceptable_range = []

    while reduce_list:
        flowname, cur_range = reduce_list.popleft()
        logging.debug(f"Reducing {flowname=} with {cur_range=}")
        if flowname not in ['A', 'R']:
            for condition in workflows[flowname]:
                logging.debug(f"Current {condition=}")
                if ':' in condition:
                    rule, potential_flow = condition.split(':')
                    new_range, opp_range = reduce_range(cur_range, rule)
                    logging.debug(f"{new_range=}\n{opp_range=}")
                    if new_range:
                        reduce_list.append([potential_flow, new_range])
                    if opp_range:
                        cur_range = opp_range
                else:
                    reduce_list.append([condition, cur_range])
        else:
            if flowname == 'A':
                acceptable_range.append(cur_range)

        logging.debug(f"Current list {reduce_list=}")
        logging.debug(f"******************************")


    total = 0
    for valid_range in acceptable_range:
        
        current = 1
        for _, value in valid_range.items():
            num = value[1] - value[0] + 1
            current *= num

        logging.debug(f"{valid_range=} {current=}")
     
        total += current

    return total



def main():
    filename = sys.argv[1]

    workflows = dict()
    parts = []
    parts_total = []

    with open(filename, 'r') as file:
        for line in file:
            if not line.startswith('{') and line.strip():
                name, flow, _ = re.split('[{}]', line)
                workflows[name] = flow.split(',')
            elif line.startswith('{'):
                x, m, a, s = line.strip().strip('[{}]').split(',')
                x = int(x.split('=')[1])
                m = int(m.split('=')[1])
                a = int(a.split('=')[1])
                s = int(s.split('=')[1])
                parts.append({'x': x, 'm': m, 'a': a, 's': s})
                parts_total.append(x+m+a+s)

    # print(f"{workflows=}")
    # print(f"{parts=}")

    part_1_res = part_1(workflows, parts, parts_total)
    part_2_res = part_2(workflows)
    print(f"{part_1_res} {part_2_res}")
                

if __name__ == "__main__":
    main()