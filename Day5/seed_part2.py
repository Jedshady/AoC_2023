#!/usr/bin/env python3 -u

# The answer is
# Day5 python ./seed_part2.py
# Calulating seed range: 3960442213 and 105867001
# Min Location: 79874951

from math import inf


def main():
    filename = "dodgy_input"
    
    mapping: dict(str, list) = dict()
    current_key = None

    with open(filename, 'r') as file:
        for line in file:
            if ':' in line:
                current_key = line.split(':')[0].split(' ')[0].strip()
                mapping[current_key] = list()
                if current_key == "seeds":
                    values = list(map(int, line.split(':')[1].strip().split(' ')))
                    mapping[current_key] = values

            elif current_key != "seeds" and line.strip():
                values = list(map(int, line.strip().split(' ')))
                mapping[current_key].append(values)


    min_location = inf
    seeds_lst = mapping["seeds"]
    for i in range(0, len(seeds_lst), 2):
        seeds = range(seeds_lst[i], seeds_lst[i] + seeds_lst[i+1], 1)
        print(f"Calulating seed range: {seeds_lst[i]} and {seeds_lst[i+1]}")
        for seed in seeds:
            # print(f"At seed: {seed}")
            soil = seed
            for seed2soil in mapping["seed-to-soil"]:
                if seed >= seed2soil[1] and seed <= seed2soil[1] + seed2soil[2] - 1:
                    soil = seed2soil[0] + (seed - seed2soil[1])
            
            fertilizer = soil
            for soil2fert in mapping["soil-to-fertilizer"]:
                if soil >= soil2fert[1] and soil <= soil2fert[1] + soil2fert[2] - 1:
                    fertilizer = soil2fert[0] + (soil - soil2fert[1])

            water = fertilizer
            for fert2water in mapping["fertilizer-to-water"]:
                if fertilizer >= fert2water[1] and fertilizer <= fert2water[1] + fert2water[2] - 1:
                    water = fert2water[0] + (fertilizer - fert2water[1])
            
            light = water
            for water2light in mapping["water-to-light"]:
                if water >= water2light[1] and water <= water2light[1] + water2light[2] - 1:
                    light = water2light[0] + (water - water2light[1])

            temperature = light
            for light2temperature in mapping["light-to-temperature"]:
                if light >= light2temperature[1] and light <= light2temperature[1] + light2temperature[2] - 1:
                    temperature = light2temperature[0] + (light - light2temperature[1])
            
            humidity = temperature
            for temp2humidity in mapping["temperature-to-humidity"]:
                if temperature >= temp2humidity[1] and temperature <= temp2humidity[1] + temp2humidity[2] - 1:
                    humidity = temp2humidity[0] + (temperature - temp2humidity[1])
        
            location = humidity
            for humidity2location in mapping["humidity-to-location"]:
                if humidity >= humidity2location[1] and humidity <= humidity2location[1] + humidity2location[2] - 1:
                    location = humidity2location[0] + (humidity - humidity2location[1])

            # print(f"Seed: {seed}, Soil: {soil}, Fert: {fertilizer}, Water: {water}, Light: {light}, Temp: {temperature}," 
                # f"Humidity: {humidity}, Location: {location}") 

            min_location = location if location < min_location else min_location 

        print(f"Min Location: {min_location}")


if __name__ == '__main__':
    main()

