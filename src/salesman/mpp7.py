import re
import time
import random


def parse_line(line):
    return [int(i) for i in re.findall('\d+', line)]


def read_file(path):
    file = open(path, 'r')
    data = list()
    file.readline()
    first_row = parse_line(file.readline())
    data.append(first_row)
    size = len(first_row)
    for i in range(size - 1):
        data_row = parse_line(file.readline())
        data.append(data_row)
    file.close()
    return data, size


def find_dist(index):
    distance = 0
    for i in range(index, num_of_cities - 1):
        distance += distances[route[i]][route[i + 1]]
    return distance


def brute_force(from_city, cities):
    if len(cities) == 1:
        return [from_city, cities[0], 0], distances[from_city][cities[0]] + distances[cities[0]][0]  # city with index 0
    min_route, min_dist = brute_force(cities[0], cities[1:])
    min_city = cities[0]
    for i in range(1, len(cities)):
        cities[0], cities[i] = cities[i], cities[0]
        candidate_route, candidate_dist = brute_force(cities[0], cities[1:])
        if candidate_dist < min_dist:
            min_dist = candidate_dist
            min_route = candidate_route
            min_city = cities[0]
        cities[i], cities[0] = cities[0], cities[i]
    return [from_city] + min_route, distances[from_city][min_city] + min_dist


def calculate_distance(route):
    distance = 0
    for i in range(1, len(route)):
        distance += distances[route[i-1]][route[i]]
    return distance


def hill_climb(iterations):
    route = [i for i in range(num_of_cities)] + [0]
    min_index = 1
    max_index = num_of_cities - 1
    best_distance = calculate_distance(route)
    for i in range(iterations):
        index1 = random.randint(min_index, max_index)
        index2 = random.randint(min_index, max_index)
        route[index1], route[index2] = route[index2], route[index1]
        candidate_distance = calculate_distance(route)
        if candidate_distance < best_distance:
            best_distance = candidate_distance
        else:
            route[index1], route[index2] = route[index2], route[index1]
    return route, best_distance


def print_result(title, circle, circle_distance, exec_time):
    print(title)
    print("route:", circle)
    print("distance:", circle_distance)
    print(f"execution time: {exec_time:0.6f} seconds")


def generate_matrix(num_of_cities):
    distances = list()
    for i in range(num_of_cities):
        row = list()
        for j in range(num_of_cities):
            if i == j:
                row.append(0)
            else:
                row.append(random.randint(1, 10))
        distances.append(row)
    return distances


def print_matrix(matrix):
    for row in matrix:
        print(row)


data_path = "small.txt"
distances, num_of_cities = read_file(data_path)

# 12: +1 m
# 13: +10 min
# 14: estimated = +2.3 h
# 15: estimated = +35 h = +1.45 d
#num_of_cities = 13
#distances = generate_matrix(num_of_cities)

print("number of cities", num_of_cities)
print_matrix(distances)

# HILL CLIMB
start = time.perf_counter()
route, dist = hill_climb(iterations=100)
end = time.perf_counter()
exec_time = end - start

print_result("HILL CLIMB", route, dist, exec_time)
print()

# BRUTE FORCE
starting_city = 0
remaining_cities = [i for i in range(1, num_of_cities)]

start = time.perf_counter()
route, dist = brute_force(starting_city, remaining_cities)
end = time.perf_counter()
exec_time = end - start

print_result("BRUTE FORCE", route, dist, exec_time)


