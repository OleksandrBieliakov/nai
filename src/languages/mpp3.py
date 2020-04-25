import os
import tkinter as tk
from tkinter import simpledialog
from perceptron import Sample
from perceptron import Perceptron


def count_letters_in_text(text):
    alphabet_len = 26
    upper_case_a = 'A'
    ascii_upper_case_a = ord(upper_case_a)
    to_lower_case = ord('a') - ord('A')

    counters = [0] * alphabet_len

    for i in range(alphabet_len):
        upper_case = chr(ascii_upper_case_a + i)
        counter = text.count(upper_case)
        lower_case = chr(ascii_upper_case_a + to_lower_case + i)
        counter += text.count(lower_case)
        counters[i] = counter
    return counters


def count_letters_in_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        text = file.read()
    return count_letters_in_text(text)


def parse_samples(directory_path):
    languages = list()
    samples = list()
    with os.scandir(directory_path) as directories:
        for directory in directories:
            if directory.is_dir():
                languages.append(directory.name)
                with os.scandir(directory) as files:
                    for file in files:
                        if file.is_file():
                            letter_counter = count_letters_in_file(file.path)
                            samples.append(Sample(attributes=letter_counter, decision=directory.name))
    return languages, samples


def normalize_sample(sample, normalization_factor=100):
    counters = sample.attributes
    letters_total = sum(counters)
    if letters_total == 0:
        print('Sample does not contain any latin letters !!!')
        return
    for index in range(len(counters)):
        counters[index] = int(counters[index] / letters_total * normalization_factor)


def normalize_samples(samples, normalization_factor=100):
    for sample in samples:
        normalize_sample(sample, normalization_factor)


def create_perceptrons(attributes_number, answer_attributes, learning_rate=1):
    perceptrons = list()
    for answer_attribute in answer_attributes:
        perceptrons.append(Perceptron(attributes_number, answer_attribute, learning_rate))
    return perceptrons


def train_perceptrons(samples, perceptrons, max_training_circles):
    for perceptron in perceptrons:
        perceptron.train(samples, max_training_circles)


# maximum selector
def check_sample(perceptrons, sample):
    max_activated_perceptron = None
    max_dot_product = -1
    for perceptron in perceptrons:
        dot_product = perceptron.find_dot_product(sample)
        if dot_product > max_dot_product:
            max_dot_product = dot_product
            max_activated_perceptron = perceptron
    if max_dot_product < 0:
        max_activated_perceptron = None
    return max_activated_perceptron


def check_test_samples(perceptrons, test_samples):
    correct_counter = 0
    for sample in test_samples:
        max_activated_perceptron = check_sample(perceptrons, sample)
        if max_activated_perceptron is not None and max_activated_perceptron.answer_attribute == sample.decision:
            correct_counter += 1
    print("Test:", correct_counter, "/", len(test_samples), "correct",
          "{:.1%}".format(correct_counter / len(test_samples)), '\n')


def classify_sample(perceptrons, sample):
    max_activated_perceptron = check_sample(perceptrons, sample)
    if max_activated_perceptron is not None:
        print('Classified as', max_activated_perceptron.answer_attribute)
    else:
        print('Not classified')


def read_input():
    root = tk.Tk()
    root.withdraw()
    text = simpledialog.askstring(title="Sample input", prompt="Enter a language sample")
    return text


def check_input_samples(perceptrons):
    accepting_input = True
    while accepting_input:
        text = read_input()
        if text is None:
            return
        sample = Sample(count_letters_in_text(text))
        normalize_sample(sample, normalization_factor=100)
        classify_sample(perceptrons, sample)


path_training_samples = r"Languages"
languages, training_samples = parse_samples(path_training_samples)
normalize_samples(training_samples, normalization_factor=100)

alphabet_len = 26
perceptrons = create_perceptrons(attributes_number=alphabet_len, answer_attributes=languages, learning_rate=1)
train_perceptrons(training_samples, perceptrons, max_training_circles=100)

path_test_samples = r"TestLanguages"
languages, test_samples = parse_samples(path_test_samples)
normalize_samples(test_samples, normalization_factor=100)

check_test_samples(perceptrons, test_samples)

check_input_samples(perceptrons)
