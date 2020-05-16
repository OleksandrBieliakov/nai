class Sample:
    def __init__(self, attributes, decision=None, distance=None, cluster=None):
        self.attributes = attributes
        self.decision = decision
        self.distance = distance
        self.cluster = cluster

    def __str__(self):
        return str(self.attributes) + " " + str(self.decision) + " " + str(self.cluster)

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
    fraction = correct / len(test_samples)
    print("Test:", correct, "/", len(test_samples), "correct", "{:.1%}".format(fraction))


def check_entered_samples(classifier):
    print("Enter attributes or 'q' to stop:")
    line = input()
    while line != "q":
        sample = parse_attributes(line)
        print("Classified as:", classifier.classified_as(sample))
        print("Enter attributes or 'q' to stop:")
        line = input()


def to_percent(measure):
    return measure * 100


def print_matrix_and_measures(matrix, measures):
    matrix_keys = list(matrix.keys())
    max_len = 0
    for key in matrix_keys:
        length = len(key)
        if length > max_len:
            max_len = length
    measures_keys = list(measures.keys())
    for key in measures_keys:
        length = len(key)
        if length > max_len:
            max_len = length
    formatting_keys = '{:' + str(max_len) + 's}'
    formatting_keys1 = '{:>' + str(max_len) + 's}'
    formatting_values = '{:' + str(max_len) + 'd}'
    formatting_values1 = '{:' + str(max_len) + '.0f}'
    print(formatting_keys.format(""), end=" ")
    for key in matrix_keys:
        print(formatting_keys1.format(key), end=" ")
    print()
    for key in matrix_keys:
        print(formatting_keys.format(key), end=" ")
        values = list(matrix[key].values())
        for val in values:
            print(formatting_values.format(val), end=" ")
        print()
    for key in measures_keys:
        print(formatting_keys.format(key), end=" ")
        for key2 in matrix_keys:
            print(formatting_values1.format(to_percent(measures[key][key2])), end=" ")
        print()


def calculate_fmeasure(precision, recall):
    return (2 * precision * recall) / (precision + recall)


def find_measures(matrix):
    keys = list(matrix.keys())
    measures = dict()
    measures_keys = ['Precision', 'Recall', 'F-measure']
    for key in measures_keys:
        measures[key] = dict()
    # precision
    for expected in keys:
        column_sum = 0
        for classified in keys:
            column_sum += matrix[classified][expected]
        measures["Precision"][expected] = matrix[expected][expected] / column_sum
    # recall
    for classified in keys:
        row_sum = 0
        for expected in keys:
            row_sum += matrix[classified][expected]
        measures["Recall"][classified] = matrix[classified][classified] / row_sum
    for key in keys:
        measures["F-measure"][key] = calculate_fmeasure(measures["Precision"][key], measures["Recall"][key])
    return measures


def check_test_samples_with_confusion_matrix(test_samples, classifier):
    correct = 0
    fails = 0
    matrix = dict()
    for decision_classified in classifier.decisions:
        matrix[decision_classified] = dict()
        for decision_expected in classifier.decisions:
            matrix[decision_classified][decision_expected] = 0
    for entry in test_samples:
        expected = entry.decision
        classified = classifier.classified_as(entry)
        matrix[classified][expected] += 1
        if expected == classified:
            correct += 1
        else:
            fails += 1
            print("FAIL", fails, ": expected -", expected, "; classified -", classified, entry.attributes)
    measures = find_measures(matrix)
    print()
    print_matrix_and_measures(matrix, measures)
    fraction = correct / len(test_samples)
    print("Accuracy:", correct, "/", len(test_samples), "correct", "{:.1%}\n".format(fraction))
