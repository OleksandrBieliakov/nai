class Sample:
    def __init__(self, attributes, decision=None, distance=None):
        self.attributes = attributes
        self.decision = decision
        self.distance = distance

    def __str__(self):
        return str(self.attributes) + " " + str(self.decision) + " " + str(self.distance)

    def __lt__(self, other):
        return self.distance < other.distance


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


def parse_attributes(line):
    attributes = line.split()
    for index in range(len(attributes)):
        attributes[index] = float(attributes[index].replace(",", "."))
    return Sample(attributes=attributes)


class IClassifier:

    def is_classified(self, sample):
        pass

    def classified_as(self, sample):
        pass


def check_test_samples(test_samples, classifier):
    correct = 0
    for entry in test_samples:
        if classifier.is_classified(entry):
            correct += 1
    print("Test:", correct, "/", len(test_samples), "correct (", correct / len(test_samples) * 100, "%)")


def check_entered_samples(classifier):
    print("Enter attributes or 'q' to stop:")
    line = input()
    while line != "q":
        sample = parse_attributes(line)
        print("Classified as:", classifier.classified_as(sample))
        print("Enter attributes or 'q' to stop:")
        line = input()
