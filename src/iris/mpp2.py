from common import read_file
from common import IClassifier
from common import check_test_samples
from common import check_entered_samples


class Perceptron:
    def __init__(self, attributes_number, answer_attribute, learning_rate=1.):
        self.weights = [0.] * attributes_number
        self.answer_attribute = answer_attribute
        self.threshold_weight = 0.
        self.learning_rate = learning_rate

    def find_dot_product(self, sample):
        dot_product = self.threshold_weight
        for weight, attribute in zip(self.weights, sample.attributes):
            dot_product += weight * attribute
        return dot_product

    def find_delta(self, sample):
        return (sample.decision == self.answer_attribute) - (self.find_dot_product(sample) >= 0)

    def adjust_weights_and_threshold(self, delta, sample):
        for index in range(len(self.weights)):
            self.weights[index] += delta * self.learning_rate * sample.attributes[index]
        self.threshold_weight += delta * self.learning_rate

    def process_sample(self, sample):
        delta = self.find_delta(sample)

        # print(str(self.weights) + " : " + str(self.threshold_weight) + " : delta " + str(delta))

        classified = False
        if delta == 0:
            classified = True
        else:
            self.adjust_weights_and_threshold(delta, sample)
        return classified

    def run_training_circle(self, samples):
        print("circle")
        all_classified = True
        for sample in samples:
            sample_classified = self.process_sample(sample)
            if not sample_classified:
                all_classified = False
        return all_classified

    def train(self, samples, max_circles):
        for circle in range(max_circles):
            # if after running a training circle all samples were classified well, we skip further weights adjustments
            circle_classified = self.run_training_circle(samples)
            if circle_classified:
                return

    def classify_sample(self, sample):
        answer = self.answer_attribute
        is_match = self.find_dot_product(sample) >= 0
        answer = answer if is_match else "NOT " + answer
        return answer


class PerceptronClassifier(IClassifier):
    def __init__(self, perceptron):
        self.perceptron = perceptron

    def is_classified(self, sample):
        expected = sample.decision == perceptron.answer_attribute
        actual = perceptron.answer_attribute == self.perceptron.classify_sample(sample)
        return expected is actual

    def classified_as(self, sample):
        return self.perceptron.classify_sample(sample)


test_path = "iris_test.txt"
training_path = "iris_training.txt"
test_samples = read_file(test_path)
training_samples = read_file(training_path)

attributes_number = len(training_samples[0].attributes)
answer_attribute = "Iris-setosa"
learning_rate = 1
perceptron = Perceptron(attributes_number, answer_attribute, learning_rate)
max_training_circles = 3
perceptron.train(training_samples, max_training_circles)

classifier = PerceptronClassifier(perceptron)
check_test_samples(test_samples, classifier)
check_entered_samples(classifier)
