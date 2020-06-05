import re
import random
import time


class DataSet:
    def __init__(self, data_set_id, sizes, values):
        self.data_set_id = data_set_id
        self.sizes = sizes
        self.values = values

    def __str__(self):
        return "Dataset " + str(self.data_set_id) + ":\n" + \
               "sizes " + str(self.sizes) + "\n" + \
               "values " + str(self.values)


def parse_line(line):
    return [int(i) for i in re.findall('\d+', line)]


def read_file(path):
    file = open(path, 'r')
    data_sets = list()
    line = file.readline()
    if line is None:
        return
    header = parse_line(line)

    line = file.readline()
    while line is not None and line != "":
        data_set_id = parse_line(line)[0]
        sizes = parse_line(file.readline())
        values = parse_line(file.readline())
        file.readline()
        line = file.readline()
        data_sets.append(DataSet(data_set_id, sizes, values))
    file.close()
    capacity_index = 1
    return header[capacity_index], data_sets


def calculate_value(data_set, result):
    value = 0
    for i in result:
        value += data_set.values[i]
    return value


def calculate_capacity(data_set, result):
    capacity = 0
    for i in result:
        capacity += data_set.sizes[i]
    return capacity


def brute_force(data_set, capacity, n):
    result = list()
    if capacity <= 0 or n < 0:
        return result, 0
    if data_set.sizes[n] > capacity:
        return brute_force(data_set, capacity, n - 1)
    skip, skip_value = brute_force(data_set, capacity, n - 1)
    include, include_value = brute_force(data_set, capacity - data_set.sizes[n], n - 1)
    include_value += data_set.values[n]
    if skip_value > include_value:
        return skip, skip_value
    include.append(n)
    return include, include_value


def print_result(data_set, result, value):
    result.sort()
    for i in result:
        print(f"nr {i} size {data_set.sizes[i]} value {data_set.values[i]}")
    print(f"total value {value}")
    print(f"capacity used {calculate_capacity(data_set, result)}")


def process_data_set(data_set, capacity):
    print("Capacity", str(capacity))
    print(data_set)
    n = len(data_set.sizes) - 1
    start = time.perf_counter()
    result, value = brute_force(data_set, capacity, n)
    end = time.perf_counter()
    print_result(data_set, result, value)
    print(f"Execution time: {end - start:0.6f} seconds")


def process_selected_data_set(data_sets, capacity):
    length = len(data_sets)
    while True:
        print("\nEnter dataset No from 1 to", str(length - 1), "or Q to quit:")
        val = input()
        if val.upper() == 'Q':
            break
        if not val.isdigit():
            continue
        data_set_index = int(val)
        if 1 <= data_set_index <= length:
            process_data_set(data_sets[data_set_index - 1], capacity)


data_sets_path = "knapsack.txt"
capacity, data_sets = read_file(data_sets_path)

data_set_index = random.randint(0, len(data_sets) - 1)
process_data_set(data_sets[data_set_index], capacity)
process_selected_data_set(data_sets, capacity)