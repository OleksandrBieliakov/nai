class Sample:
    def __init__(self, attributes, decision=None, distance=None):
        self.attributes = attributes
        self.decision = decision
        self.distance = distance

    def __str__(self):
        return str(self.attributes) + " " + str(self.decision) + " " + str(self.distance)

    def __lt__(self, other):
        return self.distance < other.distance


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
        classified = False
        if delta == 0:
            classified = True
        else:
            self.adjust_weights_and_threshold(delta, sample)
        return classified

    def run_training_circle(self, samples):
        all_classified = True
        for sample in samples:
            sample_classified = self.process_sample(sample)
            if not sample_classified:
                all_classified = False
        return all_classified

    def train(self, samples, max_circles):
        circles = 0
        for circle in range(max_circles):
            # if after running a training circle all samples were classified well, we skip further weights adjustments
            circle_classified = self.run_training_circle(samples)
            circles += 1
            if circle_classified:
                break
        print(self.answer_attribute, 'trained, epochs:', circles)
        print('weights:', self.weights)
        print()

    def classify_sample(self, sample):
        answer = self.answer_attribute
        is_match = self.find_dot_product(sample) >= 0
        answer = answer if is_match else "NOT " + answer
        return answer

    def is_activated(self, sample):
        answer = self.answer_attribute
        is_match = self.find_dot_product(sample) >= 0
        return is_match
