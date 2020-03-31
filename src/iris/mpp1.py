from common import read_file
from common import IClassifier
from common import check_test_samples
from common import check_entered_samples


def find_distance(attributes1, attributes2):
    distance = 0
    for x, y in zip(attributes1, attributes2):
        distance += (x - y) ** 2
    return distance


class KnnClassifier(IClassifier):
    def __init__(self, k, training_samples):
        self.k = k
        self.training_samples = training_samples

    def is_classified(self, sample):
        return sample.decision == self.classified_as(sample)

    def classified_as(self, sample):
        for entry in self.training_samples:
            entry.distance = find_distance(sample.attributes, entry.attributes)
        self.training_samples.sort()
        closest = self.training_samples[:k]
        samples_types = dict()
        for entry in closest:
            if entry.decision in samples_types:
                samples_types[entry.decision] += 1
            else:
                samples_types[entry.decision] = 1
        max_type = None
        max_counter = -1
        for sample_type, counter in samples_types.items():
            if counter > max_counter:
                max_counter = counter
                max_type = sample_type
        return max_type


test_path = "iris_test.txt"
training_path = "iris_training.txt"
test_samples = read_file(test_path)
training_samples = read_file(training_path)

print("Enter parameter k:")
k = int(input())

classifier = KnnClassifier(k, training_samples)
check_test_samples(test_samples, classifier)
check_entered_samples(classifier)
