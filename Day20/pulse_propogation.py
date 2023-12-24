#!/usr/bin/env python3 -u

import sys
import math
import logging
from collections import deque
from functools import reduce


logging.basicConfig(level=logging.INFO, filemode='w')


class FlipFlop:
    def __init__(self, name, scheduler) -> None:
        self.module_type = "FlipFlop"
        self.name: str = name
        self.scheduler = scheduler
        self.is_on = False  # 0: off; 1: on
        self.destinations = []
        self.pulse_sent = {"low": 0, "high": 0}

    def connect(self, module):
        self.destinations.append(module)

    def receive_pulse(self, input_name: str, pulse: str):
        if pulse == "low":
            self.is_on = not self.is_on
            if self.is_on:
                pulse_to_send = "high"
            else:
                pulse_to_send = "low"
            
            for module in self.destinations:
                logging.debug(f"Flipflop {self.name=} sending {pulse_to_send=} to {module.module_type=} {module.name=}")
                self.scheduler.add_action(self, module, pulse_to_send)
                self.pulse_sent[pulse_to_send] += 1

    def reset(self):
        self.is_on = False
        self.pulse_sent = {"low": 0, "high": 0} 


class Conjunction:
    def __init__(self, name, scheduler) -> None:
        self.module_type = "Conjunction"
        self.name: str = name
        self.scheduler = scheduler
        self.input_states = dict()
        self.destinations = []
        self.pulse_sent = {"low": 0, "high": 0}

    def add_input(self, input_name: str) -> None:
        self.input_states[input_name] = "low"

    def connect(self, module):
        self.destinations.append(module)
    
    def receive_pulse(self, input_name: str, pulse: str):
        # logging.debug(f"Conjunction {self.name=} received {input_name=} {pulse=}")
        self.input_states[input_name] = pulse
        
        if all(state == "high" for input, state in self.input_states.items()):
            pulse_to_send = "low"
        else:
            pulse_to_send = "high"

        for module in self.destinations:
            if self.name == "nc" and module.name == "rx":
                logging.debug(f"Conjunction {self.name=} sending {pulse_to_send=} to {module.module_type=} {module.name=}")
            self.scheduler.add_action(self, module, pulse_to_send)
            self.pulse_sent[pulse_to_send] += 1

    def reset(self):
        for k, _ in self.input_states.items():
            self.input_states[k] = "low"

        self.pulse_sent = {"low": 0, "high": 0}


class Broadcaster:
    def __init__(self, name, scheduler):
        self.module_type = "Broadcaster"
        self.name = name
        self.scheduler = scheduler
        self.destinations = []
        self.pulse_sent = {"low": 0, "high": 0}

    def connect(self, module):
        self.destinations.append(module)

    def receive_pulse(self, input_name: str, pulse: str):
        pulse_to_send = pulse
        for module in self.destinations:
            logging.debug(f"Broadcaster sending {pulse_to_send=} to {module.module_type=} {module.name=}")
            self.scheduler.add_action(self, module, pulse_to_send)
            self.pulse_sent[pulse_to_send] += 1

    def reset(self):
        self.pulse_sent = {"low": 0, "high": 0} 


class Button:
    def __init__(self, broadcaster, scheduler):
        self.module_type = "Button"
        self.name = "button"
        self.scheduler = scheduler
        self.destinations = [broadcaster]
        self.pulse_sent = {"low": 0, "high": 0}
 
    def press(self):
        pulse_to_send = "low"
        for module in self.destinations:
            logging.debug(f"Button sending {pulse_to_send=} to {module.module_type=} {module.name=}")
            self.scheduler.add_action(self, module, pulse_to_send)
            self.pulse_sent[pulse_to_send] += 1

    def reset(self):
        self.pulse_sent = {"low": 0, "high": 0} 


class Output:
    def __init__(self, name):
        self.module_type = "Output"
        self.name = name
        self.pulse_sent = {"low": 0, "high": 0}
        pass

    def receive_pulse(self, input_name: str, pulse: str):
        pass

    def reset(self):
        self.pulse_sent = {"low": 0, "high": 0}


class Scheduler:
    def __init__(self):
        self.name = "scheduler"
        self.module_type = "Scheduler"
        self.sequence = deque()
        self.pulse_sent = {"low": 0, "high": 0}
    
    def add_action(self, src, dst, pulse):
        self.sequence.append([src, dst, pulse])

    def finish_schedule(self):
        while self.sequence:
            src, dst, pulse_to_send = self.sequence.popleft()
            # logging.debug(f"Dealing with {src.name=} to {dst.name=} with {pulse_to_send=}")
            dst.receive_pulse(src.name, pulse_to_send)
    
    def detect_pulse(self, src_name, dst_name, pulse):
        found = False
        while self.sequence:
            src, dst, pulse_to_send = self.sequence.popleft()
            logging.debug(f"Dealing with {src.name=} to {dst.name=} with {pulse_to_send=}")

            if src.name == src_name and dst.name == dst_name and pulse_to_send == pulse:
                found = True
                return found
            dst.receive_pulse(src.name, pulse_to_send)
        return found
 

    def reset(self):
        self.sequence = deque()
        self.pulse_sent = {"low": 0, "high": 0} 


def check_FlipFlop_all_off(modules: dict()):
    all_off = True
    for name, module in modules.items():
        if isinstance(module, FlipFlop):
            logging.debug(f"{name=} {module.is_on=}")
            if module.is_on:
                all_off = False
    return all_off


def count_pulse_sent(modules: dict()):
    low_count = high_count = 0
    for _, module in modules.items():
        low_count += module.pulse_sent["low"]
        high_count += module.pulse_sent["high"]
        logging.debug(f"{module.name=} has sent {module.pulse_sent['low']=} and {module.pulse_sent['high']=}")
    return low_count, high_count


def lcm(a, b):
    return abs(a * b) // math.gcd(a, b)


def lcm_multiple(numbers):
    return reduce(lcm, numbers)


def part_1(modules, button, scheduler):
    logging.debug("*************** Initial state **************")
    assert check_FlipFlop_all_off(modules)

    # Press once
    count = 1
    logging.debug(f"*************** {count=} **************")    
    button.press()
    scheduler.finish_schedule()

    while not check_FlipFlop_all_off(modules) and count < 1000:
        count += 1
        logging.debug(f"*************** {count=} **************")
        button.press()
        scheduler.finish_schedule()


    num_of_cycle = 1000 // count
    low_count, high_count = count_pulse_sent(modules)
    total = low_count * high_count * pow(num_of_cycle, 2)
    
    logging.debug(f"{num_of_cycle=} {low_count=} {high_count=} {total=}")

    return total


def part_2(modules, connections, button, scheduler):
    dst = ''
    for k, v in connections.items():
        if "rx" in v:
            dst = k
    
    sources = []
    for k, v in connections.items():
        if dst in v:
            sources.append(k)

    # print(f"{src=} {dst=}") 

    counts = []
    for src in sources:
        for _, module in modules.items():
            module.reset()

        logging.debug("*************** Initial state **************")
        assert check_FlipFlop_all_off(modules)
 
        count = 0
        while True:
            count += 1
            logging.debug(f"*************** {count=} **************")
            button.press()
            if scheduler.detect_pulse(src, dst, "high"):
                break
        counts.append(count)

    if counts:
        return lcm_multiple(counts)
    else:
        return None


def main():
    filename = sys.argv[1]
    
    scheduler = Scheduler()
    
    modules = dict()
    connections = dict()

    with open(filename, 'r') as file:
        for line in file:
            if line.startswith('%'):
                module_name, destinations = line[1:].split(' -> ')
                modules[module_name] = FlipFlop(module_name, scheduler)
                connections[module_name] = destinations.strip().split(', ')
            elif line.startswith('&'):
                module_name, destinations = line[1:].split(' -> ')
                modules[module_name] = Conjunction(module_name, scheduler)
                connections[module_name] = destinations.strip().split(', ')
            elif "broadcaster" in line:
                module_name, destinations = line.split(' -> ')
                modules["broadcaster"] = Broadcaster(module_name, scheduler)
                connections["broadcaster"] = destinations.strip().split(', ')
 
    # Add input for Conjunctions
    for name, module in modules.items():
        if isinstance(module, Conjunction):
            for connection_name, connectioned in connections.items():
                if name in connectioned:
                    module.add_input(connection_name)

    # Add destinations for each module
    for name, destinations in connections.items():
        for destination in destinations:
            if destination not in modules:
                modules[destination] = Output(destination)
            modules[name].connect(modules[destination])

    button = Button(modules["broadcaster"], scheduler)
    modules["button"] = button
    modules["scheduler"] = scheduler
    logging.debug(f"{modules=}")
    logging.debug(f"{connections=}")
    
    part_1_res = part_1(modules, button, scheduler)

    part_2_res = part_2(modules, connections, button, scheduler)

    print(f"{part_1_res}, {part_2_res}")

                
if __name__ == "__main__":
    main()