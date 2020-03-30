class Sample:
    def __init__(self, attributes, decision=None, distance=None):
        self.attributes = attributes
        self.decision = decision
        self.distance = distance

    def __str__(self):
        return str(self.attributes) + " " + self.decision + " " + str(self.distance)

    def __lt__(self, other):
        return self.distance < other.distance


def find_distance(attributes1, attributes2):
    distance = 0
    for x, y in zip(attributes1, attributes2):
        distance += (x - y) ** 2
    return distance


def classify(sample, data, k):
    for entry in data:
        entry.distance = find_distance(sample.attributes, entry.attributes)
    data.sort()
    closest = data[:k]
    types = dict()
    for entry in closest:
        if entry.decision in types:
            types[entry.decision] += 1
        else:
            types[entry.decision] = 1
    max_type = None
    max_counter = -1
    for type, counter in types.items():
        if counter > max_counter:
            max_counter = counter
            max_type = type
    return max_type


def parse_attributes(line):
    attributes = line.split()
    for index in range(len(attributes)):
        attributes[index] = float(attributes[index].replace(",", "."))
    return Sample(attributes=attributes)


def parse_sample(line):
    attributes = line.split()
    for index in range(len(attributes) - 1):
        attributes[index] = float(attributes[index].replace(",", "."))
    return Sample(attributes=attributes[:-1], decision=attributes[-1])


def read_file(path):
    file = open(path, 'r')
    samples = list()
    for line in file:
        samples.append(parse_sample(line))
    file.close()
    return samples


test_path = "iris_test.txt"
training_path = "iris_training.txt"
test_samples = read_file(test_path)
training_samples = read_file(training_path)

print("Enter parameter k:")
k = int(input())

correct = 0
for entry in test_samples:
    if entry.decision == classify(entry, training_samples, k):
        correct += 1
print("Test:", correct, "/", len(test_samples), "correct (", correct / len(test_samples) * 100, "%)")

print("Enter attributes or 'q' to stop:")
line = input()
while line != "q":
    sample = parse_attributes(line)
    print("Classified as:", classify(sample, training_samples, k))
    print("Enter attributes or 'q' to stop:")
    line = input()
