from common import read_file
from common import IClassifier
from common import check_test_samples
from common import check_entered_samples
from common import check_test_samples_with_confusion_matrix


def grade_attributes(samples, attributes_number, num_of_grades):
    mins, maxs = find_mins_and_maxs(samples, attributes_number)
    grades = find_grades(mins, maxs, num_of_grades)
    return grades


def find_mins_and_maxs(samples, attributes_number):
    mins, maxs = list(), list()
    for i in range(attributes_number):
        attributes = list()
        for sample in samples:
            attributes.append(sample.attributes[i])
        mins.append(min(attributes))
        maxs.append(max(attributes))
    return mins, maxs


def find_grades(mins, maxs, num_of_grades):
    attributes_grades = list()
    for min, max in zip(mins, maxs):
        attribute_range = max - min
        step = attribute_range / num_of_grades
        grades = list()
        start = min
        end = min + step
        for i in range(num_of_grades):
            if i + 1 == num_of_grades:
                end = max + 1 / 16  # magic number ;) to make max < top range
            grades.append((start, end))
            start = end
            end += step
        attributes_grades.append(grades)
    return attributes_grades


def get_decisions(samples):
    decisions = set()
    for sample in samples:
        decisions.add(sample.decision)
    return decisions


def find_samples_grades(sample, grades, num_of_grades):
    attributes = sample.attributes
    sample_grades = list()
    for i in range(len(grades)):
        attribute_grades = grades[i]
        for j in range(num_of_grades):
            if attribute_grades[j][0] <= attributes[i] < attribute_grades[j][1]:
                sample_grades.append(j)
                break
            elif j == 0 and attributes[i] < attribute_grades[j][0]:
                sample_grades.append(j)
                break
            elif j == num_of_grades - 1 and attributes[i] > attribute_grades[j][1]:
                sample_grades.append(j)
                break
    return sample_grades


def find_all_samples_grades(samples, grades, num_of_grades):
    for sample in samples:
        sample.grades = find_samples_grades(sample, grades, num_of_grades)


def count_samples_grades_for_decision(samples, decision, num_of_grades):
    attributes_len = len(samples[0].attributes)
    grades_counters = list()
    for i in range(attributes_len):
        counters = dict()
        for j in range(num_of_grades):
            counters[j] = 0
        grades_counters.append(counters)

    for sample in samples:
        for i in range(attributes_len):
            attr_counters = grades_counters[i]
            for j in range(num_of_grades):
                if sample.grades[i] == j and sample.decision == decision:
                    attr_counters[j] += 1
    return grades_counters


def count_grades_for_all_decisions(samples, decisions, num_of_grades):
    counters = dict()
    for decision in decisions:
        counters[decision] = count_samples_grades_for_decision(samples, decision, num_of_grades)
    return counters


def count_decisions(samples, decisions):
    counters = dict()
    for decision in decisions:
        counters[decision] = 0
    for sample in samples:
        for decision in decisions:
            if decision == sample.decision:
                counters[decision] += 1
    return counters


def find__decisions_probabilities(samples, decisions_counters):
    total = len(samples)
    probabilities = dict()
    for key in decisions_counters.keys():
        probabilities[key] = decisions_counters[key] / total
    return probabilities


def find_all_conditioned_decisions_probabilities(samples, decisions_counters, decisions_grades_counters,
                                                 num_of_attributes_grades, attributes_number):
    final_probabilities = dict()
    for key in decisions_counters.keys():
        attributes = list()
        for i in range(attributes_number):
            grades = dict()
            for j in range(num_of_attributes_grades):
                nominator = decisions_grades_counters[key][i][j]
                denominator = decisions_counters[key]
                # simple smoothing
                if nominator == 0:
                    nominator = 1
                    denominator += num_of_attributes_grades
                grades[j] = nominator / denominator
            attributes.append(grades)
        final_probabilities[key] = attributes
    return final_probabilities


def find_conditioned_decision_probabilities(sample, all_probabilities, num_of_attributes_grades, attributes_number,
                                            decisions_probabilities):
    sample_grades = sample.grades
    final_probabilities = dict()
    for key in all_probabilities.keys():
        probabilities = [0] * attributes_number
        for i in range(attributes_number):
            for j in range(num_of_attributes_grades):
                if sample_grades[i] == j:
                    probabilities[i] = all_probabilities[key][i][j]
                    break
        probability = 1
        for pr in probabilities:
            probability *= pr
        probability *= decisions_probabilities[key]
        final_probabilities[key] = probability
    return final_probabilities


class BayesClassifier(IClassifier):
    def __init__(self, samples, num_of_grades=3):
        self.num_of_grades = num_of_grades
        self.samples = samples
        self.attributes_number = len(samples[0].attributes)
        self.grades = grade_attributes(self.samples, self.attributes_number, self.num_of_grades)
        self.decisions = get_decisions(self.samples)
        find_all_samples_grades(self.samples, self.grades, self.num_of_grades)
        self.decisions_grades_counters = count_grades_for_all_decisions(self.samples, self.decisions,
                                                                        self.num_of_grades)
        self.decisions_counters = count_decisions(self.samples, self.decisions)
        self.decisions_probabilities = find__decisions_probabilities(samples, self.decisions_counters)
        self.all_probabilities = find_all_conditioned_decisions_probabilities(self.samples, self.decisions_counters,
                                                                              self.decisions_grades_counters,
                                                                              self.num_of_grades,
                                                                              self.attributes_number)

    def is_classified(self, sample):
        return sample.decision == self.classified_as(sample)

    def classified_as(self, sample):
        sample.grades = find_samples_grades(sample, self.grades, self.num_of_grades)
        probabilities = find_conditioned_decision_probabilities(sample, self.all_probabilities, self.attributes_number,
                                                                self.num_of_grades, self.decisions_probabilities)
        max_probability = max(probabilities.values())
        for key in probabilities.keys():
            if probabilities[key] == max_probability:
                return key
        return "NOT CLASSIFIED"


test_path = "iris_test.txt"
training_path = "iris_training.txt"
test_samples = read_file(test_path)
training_samples = read_file(training_path)

classifier = BayesClassifier(training_samples)
check_test_samples_with_confusion_matrix(test_samples, classifier)
check_entered_samples(classifier)
